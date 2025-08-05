# Qumu_Elastic_Search

##Introduction##

This connector provides a simple HTTP client to interact with Elasticsearch-compatible search services via the standard Elasticsearch REST API.  It was originally developed for Bonsai and is integral to Qumu Cloud, our enterprise Video CMS for secure video management, distribution, and playback.

This connector powers indexing and search of video metadata such as Title, Tags, Description, Author with the ability to expand this to include: Transcripts and analytics allowing features such as:

Full-text transcript search across all video assets

Metadata-based filtering (e.g., tags, categories, custom fields)

Real-time analytics dashboards and reporting

By abstracting core logic, you can swap out endpoint URLs, credentials, and version-specific behaviors with minimal changes, making it ideal for any Elasticsearch-compatible service.

##Features##

- Elasticsearch HTTP API support (CRUD, search, bulk, scroll)

- Version-aware logic for Elasticsearch 7.x and 8.x compatibility

- Provider-agnostic: works with Bonsai, Elastic Cloud, AWS OpenSearch, and self-managed clusters

- Pluggable authentication: basic auth or API key out of the box


##Configuration##

Configure the connector by setting environment variables or passing a config object:

Variable    Description    Example

ES_HOST

Endpoint URL for Elasticsearch-compatible host

https://my-cluster.example.com:9243

ES_API_KEY

API key for authentication (preferred)


ES_USERNAME / ES_PASSWORD

Basic auth credentials (less secure)

admin / P@ssw0rd!

ES_TLS_VERIFY

Enable/disable certificate verification

false to skip self-signed cert checks


## Introduction

This connector provides a simple HTTP client to interact with Elasticsearch-compatible search services via the standard Elasticsearch REST API. It was originally developed for Bonsai and is integral to **Qumu Cloud**, our enterprise Video CMS for secure video management, distribution, and playback.

Within Qumu Cloud, this connector powers indexing and search of video metadata, transcript text, and analytics events—enabling features such as:

- Full-text transcript search across all video assets
- Metadata-based filtering (e.g., tags, categories, custom fields)
- Real-time analytics dashboards and reporting

By abstracting core logic, you can swap out endpoint URLs, credentials, and version-specific behaviors with minimal changes, making it ideal for any Elasticsearch-compatible service.

## Features

- **Elasticsearch HTTP API** support (CRUD, search, bulk, scroll)
- **Version-aware** logic for Elasticsearch 7.x and 8.x compatibility
- **Provider-agnostic**: works with Bonsai, Elastic Cloud, AWS OpenSearch, and self-managed clusters
- **Pluggable authentication**: basic auth or API key out of the box
- **Configurable SSL/TLS verification** options


## Installation

```bash
npm install elastic-connector
# or
pip install elastic-connector
Configuration
Configure the connector by setting environment variables or passing a config object:

Variable	Description	Example
ES_HOST	Endpoint URL for Elasticsearch-compatible host	https://my-cluster.example.com:9243
ES_API_KEY	API key for authentication (preferred)	
ES_USERNAME / ES_PASSWORD	Basic auth credentials (less secure)	admin / P@ssw0rd!
ES_TLS_VERIFY	Enable/disable certificate verification	false to skip self-signed cert checks

Authentication
This connector supports:

API Key (recommended): set via ES_API_KEY header

Basic Authentication: supply ES_USERNAME and ES_PASSWORD

Note: Using basic passwords is inherently insecure—avoid in production or ensure strong, rotated credentials.

Security Considerations
Basic Passwords: Transmitting credentials via HTTP Basic auth exposes usernames and passwords in headers; always use HTTPS and enforce TLS.

Credential Storage: Do not hard-code credentials in source. Use secure vaults or environment variables.

Certificate Verification: Disabling TLS verification (ES_TLS_VERIFY=false) exposes you to man-in-the-middle attacks.

Rate Limits: Implement exponential backoff to handle throttling; avoid hard retries.

Least Privilege: Create users with minimal permissions (e.g., index-level only).

Limitations
Does not support non-Elasticsearch vector stores (e.g., Pinecone, Qdrant, Weaviate).

Advanced features like X-Pack security, ILM, or custom ingest plugins may require additional implementation.

Extending to Other Providers
To adapt for a new Elasticsearch-compatible host:

Swap endpoint: update ES_HOST and relevant connection settings.

Adjust authentication: implement AWS SigV4, OAuth, or mTLS if required.

Verify API parity: check for differences in index templates, mappings, or query DSL.

Write an adapter: wrap core HTTP logic behind a common interface (e.g., indexDocument(), search()).

