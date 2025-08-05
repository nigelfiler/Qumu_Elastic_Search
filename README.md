## Introduction

This connector provides a simple HTTP client to interact with Elasticsearch-compatible search services via the standard Elasticsearch REST API. It was originally developed for Bonsai and is configured for **Qumu Cloud**, the enterprise Video CMS for secure video management, distribution, and playback.

This connector powers indexing and search of video content hosted in 1 or more Qumu instances and indexes metadata such as Title, Description, Tags and Publisher. It can be expanded to include Transcripts and analytics.

By abstracting core logic, you can swap out endpoint URLs, credentials, and version-specific behaviors with minimal changes, making it ideal for any Elasticsearch-compatible service.

## Features

- **Elasticsearch HTTP API** support (CRUD, search, bulk, scroll)
- **Indexes Multiple Qumu Instances** 
- **Version-aware** logic for Elasticsearch 7.x and 8.x compatibility
- **Provider-agnostic**: Tested with Bonsai but should work with Elastic Cloud, AWS OpenSearch, and self-managed clusters

## Configuration

Configure the connector by setting environment variables under the section:   
**Connect to Bonsai OpenSearch**  in: qumu_connector.py (host, port, http_auth)  
**Connect to Qumu Cloud Instance** in: run_qumu.py (domain, username, password)  
For production, replace with **oauth2.0** token
