[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=alert_status)](https://sonarcloud.io/summary?id=sdk-python-container-registry)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sdk-python-container-registry)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-container-registry)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-container-registry)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-container-registry)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-container-registry&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sdk-python-container-registry)
[![Release](https://img.shields.io/github/v/release/ionos-cloud/sdk-python-container-registry.svg)](https://github.com/ionos-cloud/sdk-python-container-registry/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/ionos-cloud/sdk-python-container-registry.svg)](https://github.com/ionos-cloud/sdk-python-container-registry/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/ionoscloud-container-registry)](https://pypi.org/project/ionoscloud-container-registry/)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")


# Python API client for ionoscloud_container_registry

## Overview
Container Registry service enables IONOS clients to manage docker and OCI
compliant registries for use by their managed Kubernetes clusters. Use a
Container Registry to ensure you have a privately accessed registry to
efficiently support image pulls.
## Changelog
### 1.1.0
 - Added new endpoints for Repositories
 - Added new endpoints for Artifacts
 - Added new endpoints for Vulnerabilities
 - Added registry vulnerabilityScanning feature


## Overview
The IONOS Cloud SDK for Python provides you with access to the IONOS Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. All API operations are performed over SSL and authenticated using your IONOS Cloud portal credentials. The API can be accessed within an instance running in IONOS Cloud or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.


### Installation & Usage

**Requirements:**
- Python >= 3.5

### pip install

Since this package is hosted on [Pypi](https://pypi.org/) you can install it by using:

```bash
pip install ionoscloud-container-registry
```

If the python package is hosted on a repository, you can install directly using:

```bash
pip install git+https://github.com/ionos-cloud/sdk-python-container-registry.git
```

Note: you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ionos-cloud/sdk-python-container-registry.git`

Then import the package:

```python
import ionoscloud_container_registry
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python setup.py install --user
```

or `sudo python setup.py install` to install the package for all users

Then import the package:

```python
import ionoscloud_container_registry
```

> **_NOTE:_**  The Python SDK does not support Python 2. It only supports Python >= 3.5.

### Authentication

The username and password **or** the authentication token can be manually specified when initializing the SDK client:

```python
configuration = ionoscloud_container_registry.Configuration(
                username='YOUR_USERNAME',
                password='YOUR_PASSWORD',
                token='YOUR_TOKEN'
                )
client = ionoscloud_container_registry.ApiClient(configuration)
```

Environment variables can also be used. This is an example of how one would do that:

```python
import os

configuration = ionoscloud_container_registry.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                token=os.environ.get('IONOS_TOKEN')
                )
client = ionoscloud_container_registry.ApiClient(configuration)
```

**Warning**: Make sure to follow the Information Security Best Practices when using credentials within your code or storing them in a file.


### HTTP proxies

You can use http proxies by setting the following environment variables:
- `IONOS_HTTP_PROXY` - proxy URL
- `IONOS_HTTP_PROXY_HEADERS` - proxy headers

Each line in `IONOS_HTTP_PROXY_HEADERS` represents one header, where the header name and value is separated by a colon. Newline characters within a value need to be escaped. See this example:
```
Connection: Keep-Alive
User-Info: MyID
User-Group: my long\nheader value
```


### Changing the base URL

Base URL for the HTTP operation can be changed in the following way:

```python
import os

configuration = ionoscloud_container_registry.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                host=os.environ.get('IONOS_API_URL'),
                server_index=None,
                )
client = ionoscloud_container_registry.ApiClient(configuration)
```

## Certificate pinning:

You can enable certificate pinning if you want to bypass the normal certificate checking procedure,
by doing the following:

Set env variable IONOS_PINNED_CERT=<insert_sha256_public_fingerprint_here>

You can get the sha256 fingerprint most easily from the browser by inspecting the certificate.


## Documentation for API Endpoints

All URIs are relative to *https://api.ionos.com/containerregistries*
<details >
    <summary title="Click to toggle">API Endpoints table</summary>


| Class | Method | HTTP request | Description |
| ------------- | ------------- | ------------- | ------------- |
| ArtifactsApi | [**registries_artifacts_get**](docs/api/ArtifactsApi.md#registries_artifacts_get) | **GET** /registries/{registryId}/artifacts | Retrieve all Artifacts by Registry |
| ArtifactsApi | [**registries_repositories_artifacts_find_by_digest**](docs/api/ArtifactsApi.md#registries_repositories_artifacts_find_by_digest) | **GET** /registries/{registryId}/repositories/{repositoryName}/artifacts/{digest} | Retrieve Artifact |
| ArtifactsApi | [**registries_repositories_artifacts_get**](docs/api/ArtifactsApi.md#registries_repositories_artifacts_get) | **GET** /registries/{registryId}/repositories/{repositoryName}/artifacts | Retrieve all Artifacts by Repository |
| ArtifactsApi | [**registries_repositories_artifacts_vulnerabilities_get**](docs/api/ArtifactsApi.md#registries_repositories_artifacts_vulnerabilities_get) | **GET** /registries/{registryId}/repositories/{repositoryName}/artifacts/{digest}/vulnerabilities | Retrieve all Vulnerabilities |
| LocationsApi | [**locations_get**](docs/api/LocationsApi.md#locations_get) | **GET** /locations | Get container registry locations |
| NamesApi | [**names_check_usage**](docs/api/NamesApi.md#names_check_usage) | **HEAD** /names/{name} | Get container registry name availability |
| RegistriesApi | [**registries_delete**](docs/api/RegistriesApi.md#registries_delete) | **DELETE** /registries/{registryId} | Delete registry |
| RegistriesApi | [**registries_find_by_id**](docs/api/RegistriesApi.md#registries_find_by_id) | **GET** /registries/{registryId} | Get a registry |
| RegistriesApi | [**registries_get**](docs/api/RegistriesApi.md#registries_get) | **GET** /registries | List all container registries |
| RegistriesApi | [**registries_patch**](docs/api/RegistriesApi.md#registries_patch) | **PATCH** /registries/{registryId} | Update the properties of a registry |
| RegistriesApi | [**registries_post**](docs/api/RegistriesApi.md#registries_post) | **POST** /registries | Create container registry |
| RegistriesApi | [**registries_put**](docs/api/RegistriesApi.md#registries_put) | **PUT** /registries/{registryId} | Create or replace a container registry |
| RepositoriesApi | [**registries_repositories_delete**](docs/api/RepositoriesApi.md#registries_repositories_delete) | **DELETE** /registries/{registryId}/repositories/{repositoryName} | Delete repository |
| RepositoriesApi | [**registries_repositories_find_by_name**](docs/api/RepositoriesApi.md#registries_repositories_find_by_name) | **GET** /registries/{registryId}/repositories/{repositoryName} | Retrieve Repository |
| RepositoriesApi | [**registries_repositories_get**](docs/api/RepositoriesApi.md#registries_repositories_get) | **GET** /registries/{registryId}/repositories | Retrieve all Repositories |
| TokensApi | [**registries_tokens_delete**](docs/api/TokensApi.md#registries_tokens_delete) | **DELETE** /registries/{registryId}/tokens/{tokenId} | Delete token |
| TokensApi | [**registries_tokens_find_by_id**](docs/api/TokensApi.md#registries_tokens_find_by_id) | **GET** /registries/{registryId}/tokens/{tokenId} | Get token information |
| TokensApi | [**registries_tokens_get**](docs/api/TokensApi.md#registries_tokens_get) | **GET** /registries/{registryId}/tokens | List all tokens for the container registry |
| TokensApi | [**registries_tokens_patch**](docs/api/TokensApi.md#registries_tokens_patch) | **PATCH** /registries/{registryId}/tokens/{tokenId} | Update token |
| TokensApi | [**registries_tokens_post**](docs/api/TokensApi.md#registries_tokens_post) | **POST** /registries/{registryId}/tokens | Create token |
| TokensApi | [**registries_tokens_put**](docs/api/TokensApi.md#registries_tokens_put) | **PUT** /registries/{registryId}/tokens/{tokenId} | Create or replace token |
| VulnerabilitiesApi | [**vulnerabilities_find_by_id**](docs/api/VulnerabilitiesApi.md#vulnerabilities_find_by_id) | **GET** /vulnerabilities/{vulnerabilityId} | Retrieve Vulnerability |

</details>

## Documentation For Models

All URIs are relative to *https://api.ionos.com/containerregistries*
<details >
<summary title="Click to toggle">API models list</summary>

 - [ApiErrorMessage](docs/models/ApiErrorMessage)
 - [ApiErrorResponse](docs/models/ApiErrorResponse)
 - [ApiResourceMetadata](docs/models/ApiResourceMetadata)
 - [Artifact](docs/models/Artifact)
 - [ArtifactMetadata](docs/models/ArtifactMetadata)
 - [ArtifactMetadataAllOf](docs/models/ArtifactMetadataAllOf)
 - [ArtifactRead](docs/models/ArtifactRead)
 - [ArtifactReadList](docs/models/ArtifactReadList)
 - [ArtifactVulnerabilityReadList](docs/models/ArtifactVulnerabilityReadList)
 - [Credentials](docs/models/Credentials)
 - [Day](docs/models/Day)
 - [Error](docs/models/Error)
 - [ErrorMessages](docs/models/ErrorMessages)
 - [Feature](docs/models/Feature)
 - [FeatureVulnerabilityScanning](docs/models/FeatureVulnerabilityScanning)
 - [Links](docs/models/Links)
 - [Location](docs/models/Location)
 - [LocationsResponse](docs/models/LocationsResponse)
 - [Metadata](docs/models/Metadata)
 - [Pagination](docs/models/Pagination)
 - [PaginationLinks](docs/models/PaginationLinks)
 - [PatchRegistryInput](docs/models/PatchRegistryInput)
 - [PatchTokenInput](docs/models/PatchTokenInput)
 - [PostRegistryInput](docs/models/PostRegistryInput)
 - [PostRegistryOutput](docs/models/PostRegistryOutput)
 - [PostRegistryProperties](docs/models/PostRegistryProperties)
 - [PostTokenInput](docs/models/PostTokenInput)
 - [PostTokenOutput](docs/models/PostTokenOutput)
 - [PostTokenProperties](docs/models/PostTokenProperties)
 - [Purl](docs/models/Purl)
 - [PutRegistryInput](docs/models/PutRegistryInput)
 - [PutRegistryOutput](docs/models/PutRegistryOutput)
 - [PutTokenInput](docs/models/PutTokenInput)
 - [PutTokenOutput](docs/models/PutTokenOutput)
 - [RegistriesResponse](docs/models/RegistriesResponse)
 - [RegistryArtifactsReadList](docs/models/RegistryArtifactsReadList)
 - [RegistryFeatures](docs/models/RegistryFeatures)
 - [RegistryPagination](docs/models/RegistryPagination)
 - [RegistryProperties](docs/models/RegistryProperties)
 - [RegistryResponse](docs/models/RegistryResponse)
 - [Repository](docs/models/Repository)
 - [RepositoryMetadata](docs/models/RepositoryMetadata)
 - [RepositoryMetadataAllOf](docs/models/RepositoryMetadataAllOf)
 - [RepositoryRead](docs/models/RepositoryRead)
 - [RepositoryReadList](docs/models/RepositoryReadList)
 - [Scope](docs/models/Scope)
 - [StorageUsage](docs/models/StorageUsage)
 - [TokenProperties](docs/models/TokenProperties)
 - [TokenResponse](docs/models/TokenResponse)
 - [TokensResponse](docs/models/TokensResponse)
 - [Vulnerability](docs/models/Vulnerability)
 - [VulnerabilityDataSource](docs/models/VulnerabilityDataSource)
 - [VulnerabilityMetadata](docs/models/VulnerabilityMetadata)
 - [VulnerabilityRead](docs/models/VulnerabilityRead)
 - [VulnerabilityReadList](docs/models/VulnerabilityReadList)
 - [WeeklySchedule](docs/models/WeeklySchedule)


[[Back to API list]](#documentation-for-api-endpoints) [[Back to Model list]](#documentation-for-models)

</details>