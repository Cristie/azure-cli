# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.profiles import PROFILE_TYPE, supported_api_version
from azure.cli.core.sdk.util import CliCommandType

from ._client_factory import cf_cdn


def load_command_table(self, command):

    def _not_found(message):
        def _inner_not_found(ex):
            from azure.mgmt.cdn.models.error_response import ErrorResponseException
            from knack.util import CLIError

            if isinstance(ex, ErrorResponseException) \
                    and ex.response is not None \
                    and ex.response.status_code == 404:
                raise CLIError(message)
            raise ex
        return _inner_not_found


    not_found_msg = "{}(s) not found. Please verify the resource(s), group or it's parent resources " \
                    "exist."
    profile_not_found_msg = not_found_msg.format('Profile')
    endpoint_not_found_msg = not_found_msg.format('Endpoint')
    cd_not_found_msg = not_found_msg.format('Custom Domain')
    origin_not_found_msg = not_found_msg.format('Origin')

    cdn_custom = CliCommandType(operations_tmpl='azure.cli.command_modules.cdn.custom#{}')
    cdn_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn#CdnManagementClient.{}',
        client_factory=cf_cdn
    )

    cdn_endpoints_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn.operations.endpoints_operations#EndpointsOperations.{}',
        client_factory=cf_cdn,
        exception_handler=_not_found(endpoint_not_found_msg)
    )

    cdn_profiles_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn.operations.profiles_operations#ProfilesOperations.{}',
        client_factory=cf_cdn,
        exception_handler=_not_found(profile_not_found_msg)
    )

    cdn_domain_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn.operations.custom_domains_operations#CustomDomainsOperations.{}',
        client_factory=cf_cdn,
        exception_handler=_not_found(cd_not_found_msg)
    )

    cdn_origin_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn.operations.origins_operations#OriginsOperations.{}',
        client_factory=cf_cdn,
        exception_handler=_not_found(origin_not_found_msg)
    )

    cdn_edge_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.cdn.operations.edge_nodes_operations#EdgeNodesOperations.{}',
        client_factory=cf_cdn
    )

    with self.command_group('cdn', cdn_sdk) as g:
        g.command('name-exists', 'check_name_availability')
        g.command('usage', 'check_resource_usage')

    with self.command_group('cdn endpoint', cdn_sdk) as g:
        for name in ['start', 'stop', 'delete']:
            g.command(name, name)
        g.command('show', 'get')
        g.command('list', 'list_by_profile')
        g.command('load', 'load_content')
        g.command('purge', 'purge_content')
        g.command('validate-custom-domain', 'validate_custom_domain')
        g.command('create', 'create_endpoint', command_type=cdn_custom)
        #g.generic_update_command('update', 'get', 'update', custom_func_name='update_endpoint',
        #                            setter_arg_name='endpoint_update_properties')

    with self.command_group('cdn profile', cdn_profiles_sdk) as g:
        g.command('show', 'get')
        g.command('usage', 'list_resource_usage')
        g.command('delete', 'delete')
        g.command('list', 'list_profiles', command_type=cdn_custom)
        g.command('create', 'create_profile', command_type=cdn_custom)
        #g.generic_update_command('update', 'get', 'update', custom_func_name='update_profile')

    with self.command_group('cdn custom-domain', cdn_domain_sdk) as g:
        g.command('show', 'get')
        g.command('delete', 'delete')
        g.command('list', 'list_by_endpoint')
        g.command('create', 'create_custom_domain', command_type=cdn_custom)

    with self.command_group('cdn origin', cdn_origin_sdk) as g:
        g.command('show', 'get')
        g.command('list', 'list_by_endpoint')

    with self.command_group('cdn edge-node', cdn_edge_sdk) as g:
        g.command('list', 'list')
