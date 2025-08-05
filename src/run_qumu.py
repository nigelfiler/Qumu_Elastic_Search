    
import asyncio
from qumu_connector import QumuClient, index_to_bonsai, es, INDEX_NAME


async def run():
 
    configs = [
        {"domain": "aaa.qumucloud.com", "username": "john.doe", "password": "my-password"},
        {"domain": "bbb.qumucloud.com", "username": "john.doe", "password": "my-password"},
        {"domain": "ccc.qumucloud.com", "username": "john.doe", "password": "my-password"},
        {"domain": "ddd.qumucloud.com", "username": "john.doe", "password": "my-password"},
    ]

    for config in configs:
        client = QumuClient(config["domain"], config["username"], config["password"])
        async for kulu in client.list_kulus(days=31):
            await index_to_bonsai(kulu, config["domain"])
        await client.close()

if __name__ == "__main__":
    asyncio.run(run())
