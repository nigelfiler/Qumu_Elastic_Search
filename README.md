## Introduction

This connector provides a simple HTTP client to interact with Elasticsearch-compatible search services via the standard Elasticsearch REST API. It was originally developed for Bonsai and is configured for **Qumu Cloud**, the enterprise Video CMS for secure video management, distribution, and playback.

This connector powers indexing and search of video content hosted in 1 or more Qumu instances and indexes metadata such as Title, Description, Tags and Publisher. It can be expanded to include Transcripts and analytics.

By abstracting core logic, you can swap out endpoint URLs, credentials, and version-specific behaviors with minimal changes, making it ideal for any Elasticsearch-compatible service.

**This sample is neither endorsed or supported by Qumu.**


## Features

- **Elasticsearch HTTP API** support (CRUD, search, bulk, scroll)
- **Indexes Multiple Qumu Instances** 
- **Version-aware** logic for Elasticsearch 7.x and 8.x compatibility
- **Provider-agnostic**: Tested with Bonsai but should work with Elastic Cloud, AWS OpenSearch, and self-managed clusters


## Configuration

Configure the connector by setting environment variables under the section:   
- **Connect to Bonsai OpenSearch**  in: qumu_connector.py (host, port, http_auth)  
- **Connect to Qumu Cloud Instance** in: run_qumu.py (domain, username, password)  

For production, replace with **OAuth2.0 bearer tokens** which are more secure.



## Scheduled Indexing

To keep your search index up to date with the latest Qumu Cloud video content, run the connector on a recurring schedule as a background process. Here’s how to do it in simple terms:

- Set a regular interval: Decide how often you need to update your index (for example, hourly or daily).

- Fetch new data: Each time the process runs, it should retrieve only the new or changed video records—such as recently uploaded videos, updated metadata, or fresh transcripts—from Qumu Cloud.

- Send to Elasticsearch: The process then sends these records to your Elasticsearch-compatible service to add or update the index.

- Automate execution: Use your environment’s scheduler (for instance, a cron job on Linux or a scheduled task in a container orchestration platform) to launch the connector automatically at the chosen interval.

- Monitor and alert: Implement simple checks so that if the process fails—due to network issues or authentication problems—you receive an alert (for example, an email or a message in your monitoring dashboard).
