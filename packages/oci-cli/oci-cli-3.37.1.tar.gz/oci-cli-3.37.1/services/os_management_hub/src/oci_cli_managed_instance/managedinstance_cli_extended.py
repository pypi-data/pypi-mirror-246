# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import click  # noqa: F401
import json  # noqa: F401
from services.os_management_hub.src.oci_cli_managed_instance.generated import managedinstance_cli
from services.os_management_hub.src.oci_cli_os_management_hub.generated import os_management_hub_service_cli
from oci_cli import cli_util  # noqa: F401
from oci_cli import custom_types  # noqa: F401
from oci_cli import json_skeleton_utils  # noqa: F401


# oci os-management-hub managed-instance managed-instance install-module-stream-profile -> oci os-management-hub managed-instance managed-instance install-module-profile
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.install_module_stream_profile_on_managed_instance, "install-module-profile")


# oci os-management-hub managed-instance managed-instance list-managed-instance-available-packages -> oci os-management-hub managed-instance managed-instance list-available-packages
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_available_packages, "list-available-packages")


# oci os-management-hub managed-instance managed-instance list-managed-instance-available-software-sources -> oci os-management-hub managed-instance managed-instance list-available-software-sources
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_available_software_sources, "list-available-software-sources")


# oci os-management-hub managed-instance managed-instance list-managed-instance-errata -> oci os-management-hub managed-instance managed-instance list-errata
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_errata, "list-errata")


# oci os-management-hub managed-instance managed-instance list-managed-instance-installed-packages -> oci os-management-hub managed-instance managed-instance list-installed-packages
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_installed_packages, "list-installed-packages")


# oci os-management-hub managed-instance managed-instance list-managed-instance-modules -> oci os-management-hub managed-instance managed-instance list-modules
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_modules, "list-modules")


# oci os-management-hub managed-instance managed-instance list-managed-instance-updatable-packages -> oci os-management-hub managed-instance managed-instance list-updatable-packages
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.list_managed_instance_updatable_packages, "list-updatable-packages")


# oci os-management-hub managed-instance managed-instance update-all-packages-on-managed-instances-in-compartment -> oci os-management-hub managed-instance managed-instance update-all-packages-in-compartment
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.update_all_packages_on_managed_instances_in_compartment, "update-all-packages-in-compartment")


# oci os-management-hub managed-instance managed-instance attach -> oci os-management-hub managed-instance managed-instance attach-software-sources
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.attach_software_sources_to_managed_instance, "attach-software-sources")


# oci os-management-hub managed-instance managed-instance detach -> oci os-management-hub managed-instance managed-instance detach-software-sources
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.detach_software_sources_from_managed_instance, "detach-software-sources")


# oci os-management-hub managed-instance managed-instance remove -> oci os-management-hub managed-instance managed-instance remove-packages
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.remove_packages_from_managed_instance, "remove-packages")


# Remove manage-module-streams from oci os-management-hub managed-instance managed-instance
managedinstance_cli.managed_instance_group.commands.pop(managedinstance_cli.manage_module_streams_on_managed_instance.name)


# Move commands under 'oci os-management-hub managed-instance managed-instance' -> 'oci os-management-hub managed-instance'
managedinstance_cli.managed_instance_root_group.commands.pop(managedinstance_cli.managed_instance_group.name)

os_management_hub_service_cli.os_management_hub_service_group.commands.pop(managedinstance_cli.managed_instance_root_group.name)
os_management_hub_service_cli.os_management_hub_service_group.add_command(managedinstance_cli.managed_instance_group)


@cli_util.copy_params_from_generated_command(managedinstance_cli.list_managed_instances, params_to_exclude=['is_attached_to_group_or_lifecycle_stage', 'lifecycle_stage', 'lifecycle_stage_not_equal_to', 'group_not_equal_to'])
@managedinstance_cli.managed_instance_group.command(name=managedinstance_cli.list_managed_instances.name, help=managedinstance_cli.list_managed_instances.help)
@cli_util.option('--is-attached-to-group-or-stage', type=click.BOOL, help=u"""A filter to return only managed instances that are attached to the specified group or lifecycle environment.""")
@cli_util.option('--stage', type=click.BOOL, help=u"""A filter to return only managed instances that are associated with the specified lifecycle environment.""")
@cli_util.option('--stage-ne', help=u"""A filter to return only managed instances that are NOT associated with the specified lifecycle environment.""")
@cli_util.option('--group-ne', help=u"""A filter to return only managed instances that are NOT attached to the specified group.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'display-name': {'module': 'os_management_hub', 'class': 'list[string]'}, 'advisory-name': {'module': 'os_management_hub', 'class': 'list[string]'}}, output_type={'module': 'os_management_hub', 'class': 'ManagedInstanceCollection'})
@cli_util.wrap_exceptions
def list_managed_instances_extended(ctx, **kwargs):

    if 'is_attached_to_group_or_stage' in kwargs:
        kwargs['is_attached_to_group_or_lifecycle_stage'] = kwargs['is_attached_to_group_or_stage']
        kwargs.pop('is_attached_to_group_or_stage')

    if 'stage' in kwargs:
        kwargs['lifecycle_stage'] = kwargs['stage']
        kwargs.pop('stage')

    if 'stage_ne' in kwargs:
        kwargs['lifecycle_stage_not_equal_to'] = kwargs['stage_ne']
        kwargs.pop('stage_ne')

    if 'group_ne' in kwargs:
        kwargs['group_not_equal_to'] = kwargs['group_ne']
        kwargs.pop('group_ne')

    ctx.invoke(managedinstance_cli.list_managed_instances, **kwargs)


@cli_util.copy_params_from_generated_command(managedinstance_cli.update_managed_instance, params_to_exclude=['primary_management_station_id', 'secondary_management_station_id'])
@managedinstance_cli.managed_instance_group.command(name=managedinstance_cli.update_managed_instance.name, help=managedinstance_cli.update_managed_instance.help)
@cli_util.option('--primary-station-id', help=u"""The OCID of a management station to be used as the preferred primary.""")
@cli_util.option('--secondary-station-id', help=u"""The OCID of a management station to be used as the preferred secondary.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'os_management_hub', 'class': 'ManagedInstance'})
@cli_util.wrap_exceptions
def update_managed_instance_extended(ctx, **kwargs):

    if 'primary_station_id' in kwargs:
        kwargs['primary_management_station_id'] = kwargs['primary_station_id']
        kwargs.pop('primary_station_id')

    if 'secondary_station_id' in kwargs:
        kwargs['secondary_management_station_id'] = kwargs['secondary_station_id']
        kwargs.pop('secondary_station_id')

    ctx.invoke(managedinstance_cli.update_managed_instance, **kwargs)


@cli_util.copy_params_from_generated_command(managedinstance_cli.list_managed_instance_modules, params_to_exclude=['name', 'name_contains'])
@managedinstance_cli.managed_instance_group.command(name=managedinstance_cli.list_managed_instance_modules.name, help=managedinstance_cli.list_managed_instance_modules.help)
@cli_util.option('--module-name', help=u"""The resource name.""")
@cli_util.option('--module-name-contains', help=u"""A filter to return resources that may partially match the name given.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'os_management_hub', 'class': 'ManagedInstanceModuleCollection'})
@cli_util.wrap_exceptions
def list_managed_instance_modules_extended(ctx, **kwargs):

    if 'module_name' in kwargs:
        kwargs['name'] = kwargs['module_name']
        kwargs.pop('module_name')

    if 'module_name_contains' in kwargs:
        kwargs['name_contains'] = kwargs['module_name_contains']
        kwargs.pop('module_name_contains')

    ctx.invoke(managedinstance_cli.list_managed_instance_modules, **kwargs)


# Rename remove to remove-module-profile
cli_util.rename_command(managedinstance_cli, managedinstance_cli.managed_instance_group, managedinstance_cli.remove_module_stream_profile_from_managed_instance, "remove-module-profile")


# Move oci os-management-hub managed-instance update-all-packages-on-managed-instances-in-compartment to oci os-management-hub update-all-packages-on-managed-instances-in-compartment
managedinstance_cli.managed_instance_group.commands.pop(managedinstance_cli.update_all_packages_on_managed_instances_in_compartment.name)
os_management_hub_service_cli.os_management_hub_service_group.add_command(managedinstance_cli.update_all_packages_on_managed_instances_in_compartment)
