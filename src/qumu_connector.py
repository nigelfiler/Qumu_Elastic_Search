import os
from contextlib import asynccontextmanager
from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from opensearchpy import OpenSearch

import logging
logger = logging.getLogger("qumu_connector")

# Utilities (minimal replacements for missing connectors.utils)
class CancellableSleeps:
    def cancel(self):
        pass

def iso_utc(dt):
    return dt.isoformat()

RETRIES = 3
RETRY_INTERVAL = 2
PAGE_SIZE = 100

# Connect to Bonsai OpenSearch
es = OpenSearch(
    hosts=[{
        "host": "my-server.eu-west-1.bonsaisearch.net",
        "port": 443
    }],
    http_auth=("cluster-access-key", "cluster-access-secret"),
    use_ssl=True,
    verify_certs=True
)

INDEX_NAME = "qumu-content"

# Ensure index exists
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

async def index_to_bonsai(kulu, instance):
    try:
        video = {
            "guid": kulu.get("guid"),
            "title": kulu.get("title"),
            "description": next((m.get("value") for m in kulu.get("metadata", []) if m.get("title") == "Description"), ""),
            "tags": next((m.get("value") for m in kulu.get("metadata", []) if m.get("title") == "Tags"), []),
            "publisher": kulu.get("publisher", {}).get("name", ""),
            "duration": kulu.get("duration"),
            "published": kulu.get("published"),
            "instance": instance
        }

        result = es.index(index=INDEX_NAME, id=kulu["guid"] + "@" + instance, body=video)
        print(f"Indexed Qumu video: {result['_id']}")
    except Exception as e:
        print(f"Failed to index: {e}")

def purge_duplicates():
    print("Purging duplicate documents...")
    seen_ids = set()
    all_docs = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}, "size": 1000, "sort": ["_id"]})
    hits = all_docs.get("hits", {}).get("hits", [])
    for hit in hits:
        doc_id = hit["_id"]
        if doc_id in seen_ids:
            es.delete(index=INDEX_NAME, id=doc_id)
            print(f"Deleted duplicate document ID: {doc_id}")
        else:
            seen_ids.add(doc_id)
    print(f"Purge complete. {len(seen_ids)} unique documents retained.")

class QumuResourceNotFound(Exception):
    pass

class QumuAPISession:
    def __init__(self, http_session, username, password, logger_):
        self._session = http_session
        self._username = username
        self._password = password
        self._logger = logger_
        self._sleeps = CancellableSleeps()

    def set_logger(self, logger_):
        self._logger = logger_

    def close(self):
        self._sleeps.cancel()

    async def _get(self, url):
        try:
            auth = aiohttp.BasicAuth(self._username, self._password)
            async with self._session.get(url, auth=auth) as resp:
                resp.raise_for_status()
                return await resp.json()
        except ClientResponseError as ex:
            if ex.status == 404:
                raise QumuResourceNotFound(f"Resource not found: {url}") from ex
            raise

    async def fetch_json(self, url):
        try:
            return await self._get(url)
        except Exception as e:
            self._logger.warning(f"Skipping URL {url}, error: {e}")

    async def scroll(self, url):
        next_url = url
        while next_url:
            data = await self.fetch_json(next_url)
            if not data:
                break
            yield data
            next_url = data.get('nextPage', {}).get('href')

class QumuClient:
    def __init__(self, domain, username, password):
        self._logger = logger
        self.domain = domain
        self.api_base = f"https://{domain}/api/2.2/rest"
        self._session = aiohttp.ClientSession(raise_for_status=True)
        self.api = QumuAPISession(
            http_session=self._session,
            username=username,
            password=password,
            logger_=self._logger,
        )

    def set_logger(self, logger_):
        self._logger = logger_
        self.api.set_logger(logger_)

    async def close(self):
        await self._session.close()
        self.api.close()

    async def list_kulus(self, days=31):
        url = f"{self.api_base}/kulus?search=published,in_the_last,{days},days&limit={PAGE_SIZE}"
        async for page in self.api.scroll(url):
            for k in page.get('kulus', []):
                yield k

    async def get_kulu_details(self, guid):
        url = f"{self.api_base}/kulus/{guid}"
        return await self.api.fetch_json(url)