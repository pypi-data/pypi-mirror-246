from __future__ import absolute_import

import re  # noqa: F401
import six

from ionoscloud_container_registry.api_client import ApiClient
from ionoscloud_container_registry.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class RepositoriesApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def registries_repositories_delete(self, registry_id, repository_name, **kwargs):  # noqa: E501
        """Delete repository  # noqa: E501

        Delete all repository contents    The registry V2 API allows manifests and blobs to be deleted individually but it is not possible to remove an entire repository.   This operation is provided for convenience  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_delete(registry_id, repository_name, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param repository_name: The name of the repository (required)
        :type repository_name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_repositories_delete_with_http_info(registry_id, repository_name, **kwargs)  # noqa: E501

    def registries_repositories_delete_with_http_info(self, registry_id, repository_name, **kwargs):  # noqa: E501
        """Delete repository  # noqa: E501

        Delete all repository contents    The registry V2 API allows manifests and blobs to be deleted individually but it is not possible to remove an entire repository.   This operation is provided for convenience  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_delete_with_http_info(registry_id, repository_name, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param repository_name: The name of the repository (required)
        :type repository_name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'repository_name'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_repositories_delete" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_repositories_delete`")  # noqa: E501
        # verify the required parameter 'repository_name' is set
        if self.api_client.client_side_validation and ('repository_name' not in local_var_params or  # noqa: E501
                                                        local_var_params['repository_name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `repository_name` when calling `registries_repositories_delete`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_repositories_delete`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'repository_name' in local_var_params and not re.search(r'^[a-z0-9]+(?:[._-][a-z0-9]+)*$', local_var_params['repository_name']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `repository_name` when calling `registries_repositories_delete`, must conform to the pattern `/^[a-z0-9]+(?:[._-][a-z0-9]+)*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'repository_name' in local_var_params:
            path_params['repositoryName'] = local_var_params['repository_name']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = None
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/repositories/{repositoryName}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_repositories_find_by_name(self, registry_id, repository_name, **kwargs):  # noqa: E501
        """Retrieve Repository  # noqa: E501

        Returns the Repository by Name.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_find_by_name(registry_id, repository_name, async_req=True)
        >>> result = thread.get()

        :param registry_id: The ID (UUID) of the Registry. (required)
        :type registry_id: str
        :param repository_name: The Name of the Repository that should be retrieved. (required)
        :type repository_name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: RepositoryRead
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_repositories_find_by_name_with_http_info(registry_id, repository_name, **kwargs)  # noqa: E501

    def registries_repositories_find_by_name_with_http_info(self, registry_id, repository_name, **kwargs):  # noqa: E501
        """Retrieve Repository  # noqa: E501

        Returns the Repository by Name.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_find_by_name_with_http_info(registry_id, repository_name, async_req=True)
        >>> result = thread.get()

        :param registry_id: The ID (UUID) of the Registry. (required)
        :type registry_id: str
        :param repository_name: The Name of the Repository that should be retrieved. (required)
        :type repository_name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(RepositoryRead, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'repository_name'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_repositories_find_by_name" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_repositories_find_by_name`")  # noqa: E501
        # verify the required parameter 'repository_name' is set
        if self.api_client.client_side_validation and ('repository_name' not in local_var_params or  # noqa: E501
                                                        local_var_params['repository_name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `repository_name` when calling `registries_repositories_find_by_name`")  # noqa: E501

        if self.api_client.client_side_validation and ('repository_name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['repository_name']) > 256):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `repository_name` when calling `registries_repositories_find_by_name`, length must be less than or equal to `256`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'repository_name' in local_var_params:
            path_params['repositoryName'] = local_var_params['repository_name']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'RepositoryRead'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/repositories/{repositoryName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_repositories_get(self, registry_id, **kwargs):  # noqa: E501
        """Retrieve all Repositories  # noqa: E501

        This endpoint enables retrieving all Repositories using pagination and optional filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_get(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The ID (UUID) of the Registry. (required)
        :type registry_id: str
        :param offset: The first element (of the total list of elements) to include in the response. Use together with limit for pagination.
        :type offset: int
        :param limit: The maximum number of elements to return. Use together with offset for pagination.
        :type limit: int
        :param filter_name: Filter resources by name.
        :type filter_name: str
        :param filter_vulnerability_severity: Filter resources by vulnerability severity.
        :type filter_vulnerability_severity: str
        :param order_by: The field to order the results by. If not provided, the results will be ordered by the default field.
        :type order_by: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: RepositoryReadList
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_repositories_get_with_http_info(registry_id, **kwargs)  # noqa: E501

    def registries_repositories_get_with_http_info(self, registry_id, **kwargs):  # noqa: E501
        """Retrieve all Repositories  # noqa: E501

        This endpoint enables retrieving all Repositories using pagination and optional filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_repositories_get_with_http_info(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The ID (UUID) of the Registry. (required)
        :type registry_id: str
        :param offset: The first element (of the total list of elements) to include in the response. Use together with limit for pagination.
        :type offset: int
        :param limit: The maximum number of elements to return. Use together with offset for pagination.
        :type limit: int
        :param filter_name: Filter resources by name.
        :type filter_name: str
        :param filter_vulnerability_severity: Filter resources by vulnerability severity.
        :type filter_vulnerability_severity: str
        :param order_by: The field to order the results by. If not provided, the results will be ordered by the default field.
        :type order_by: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(RepositoryReadList, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'offset',
            'limit',
            'filter_name',
            'filter_vulnerability_severity',
            'order_by'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_repositories_get" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_repositories_get`")  # noqa: E501

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `registries_repositories_get`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 1000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `registries_repositories_get`, must be a value less than or equal to `1000`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `registries_repositories_get`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'filter_name' in local_var_params and local_var_params['filter_name'] is not None:  # noqa: E501
            query_params.append(('filter.name', local_var_params['filter_name']))  # noqa: E501
        if 'filter_vulnerability_severity' in local_var_params and local_var_params['filter_vulnerability_severity'] is not None:  # noqa: E501
            query_params.append(('filter.vulnerabilitySeverity', local_var_params['filter_vulnerability_severity']))  # noqa: E501
        if 'order_by' in local_var_params and local_var_params['order_by'] is not None:  # noqa: E501
            query_params.append(('orderBy', local_var_params['order_by']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'RepositoryReadList'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/repositories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
