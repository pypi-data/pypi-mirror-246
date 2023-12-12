# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['IncidentWorkflowTriggerArgs', 'IncidentWorkflowTrigger']

@pulumi.input_type
class IncidentWorkflowTriggerArgs:
    def __init__(__self__, *,
                 subscribed_to_all_services: pulumi.Input[bool],
                 type: pulumi.Input[str],
                 workflow: pulumi.Input[str],
                 condition: Optional[pulumi.Input[str]] = None,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a IncidentWorkflowTrigger resource.
        :param pulumi.Input[bool] subscribed_to_all_services: Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        :param pulumi.Input[str] type: [Updating causes resource replacement] May be either `manual` or `conditional`.
        :param pulumi.Input[str] workflow: The workflow ID for the workflow to trigger.
        :param pulumi.Input[str] condition: A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        """
        pulumi.set(__self__, "subscribed_to_all_services", subscribed_to_all_services)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "workflow", workflow)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if services is not None:
            pulumi.set(__self__, "services", services)

    @property
    @pulumi.getter(name="subscribedToAllServices")
    def subscribed_to_all_services(self) -> pulumi.Input[bool]:
        """
        Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        """
        return pulumi.get(self, "subscribed_to_all_services")

    @subscribed_to_all_services.setter
    def subscribed_to_all_services(self, value: pulumi.Input[bool]):
        pulumi.set(self, "subscribed_to_all_services", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        [Updating causes resource replacement] May be either `manual` or `conditional`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def workflow(self) -> pulumi.Input[str]:
        """
        The workflow ID for the workflow to trigger.
        """
        return pulumi.get(self, "workflow")

    @workflow.setter
    def workflow(self, value: pulumi.Input[str]):
        pulumi.set(self, "workflow", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input[str]]:
        """
        A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def services(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        """
        return pulumi.get(self, "services")

    @services.setter
    def services(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "services", value)


@pulumi.input_type
class _IncidentWorkflowTriggerState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input[str]] = None,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subscribed_to_all_services: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IncidentWorkflowTrigger resources.
        :param pulumi.Input[str] condition: A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        :param pulumi.Input[bool] subscribed_to_all_services: Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        :param pulumi.Input[str] type: [Updating causes resource replacement] May be either `manual` or `conditional`.
        :param pulumi.Input[str] workflow: The workflow ID for the workflow to trigger.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if services is not None:
            pulumi.set(__self__, "services", services)
        if subscribed_to_all_services is not None:
            pulumi.set(__self__, "subscribed_to_all_services", subscribed_to_all_services)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if workflow is not None:
            pulumi.set(__self__, "workflow", workflow)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input[str]]:
        """
        A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def services(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        """
        return pulumi.get(self, "services")

    @services.setter
    def services(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "services", value)

    @property
    @pulumi.getter(name="subscribedToAllServices")
    def subscribed_to_all_services(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        """
        return pulumi.get(self, "subscribed_to_all_services")

    @subscribed_to_all_services.setter
    def subscribed_to_all_services(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "subscribed_to_all_services", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] May be either `manual` or `conditional`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def workflow(self) -> Optional[pulumi.Input[str]]:
        """
        The workflow ID for the workflow to trigger.
        """
        return pulumi.get(self, "workflow")

    @workflow.setter
    def workflow(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workflow", value)


class IncidentWorkflowTrigger(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[str]] = None,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subscribed_to_all_services: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An [Incident Workflow Trigger](https://support.pagerduty.com/docs/incident-workflows#triggers) defines when and if an [Incident Workflow](https://support.pagerduty.com/docs/incident-workflows) will be triggered.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        my_first_workflow = pagerduty.IncidentWorkflow("myFirstWorkflow",
            description="This Incident Workflow is an example",
            steps=[pagerduty.IncidentWorkflowStepArgs(
                name="Send Status Update",
                action="pagerduty.com:incident-workflows:send-status-update:1",
                inputs=[pagerduty.IncidentWorkflowStepInputArgs(
                    name="Message",
                    value="Example status message sent on {{current_date}}",
                )],
            )])
        first_service = pagerduty.get_service(name="My First Service")
        automatic_trigger = pagerduty.IncidentWorkflowTrigger("automaticTrigger",
            type="conditional",
            workflow=my_first_workflow.id,
            services=[pagerduty_service["first_service"]["id"]],
            condition="incident.priority matches 'P1'",
            subscribed_to_all_services=False)
        devops = pagerduty.get_team(name="devops")
        manual_trigger = pagerduty.IncidentWorkflowTrigger("manualTrigger",
            type="manual",
            workflow=my_first_workflow.id,
            services=[pagerduty_service["first_service"]["id"]])
        ```

        ## Import

        Incident workflows can be imported using the `id`, e.g.

        ```sh
         $ pulumi import pagerduty:index/incidentWorkflowTrigger:IncidentWorkflowTrigger pagerduty_incident_workflow_trigger PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] condition: A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        :param pulumi.Input[bool] subscribed_to_all_services: Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        :param pulumi.Input[str] type: [Updating causes resource replacement] May be either `manual` or `conditional`.
        :param pulumi.Input[str] workflow: The workflow ID for the workflow to trigger.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IncidentWorkflowTriggerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An [Incident Workflow Trigger](https://support.pagerduty.com/docs/incident-workflows#triggers) defines when and if an [Incident Workflow](https://support.pagerduty.com/docs/incident-workflows) will be triggered.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        my_first_workflow = pagerduty.IncidentWorkflow("myFirstWorkflow",
            description="This Incident Workflow is an example",
            steps=[pagerduty.IncidentWorkflowStepArgs(
                name="Send Status Update",
                action="pagerduty.com:incident-workflows:send-status-update:1",
                inputs=[pagerduty.IncidentWorkflowStepInputArgs(
                    name="Message",
                    value="Example status message sent on {{current_date}}",
                )],
            )])
        first_service = pagerduty.get_service(name="My First Service")
        automatic_trigger = pagerduty.IncidentWorkflowTrigger("automaticTrigger",
            type="conditional",
            workflow=my_first_workflow.id,
            services=[pagerduty_service["first_service"]["id"]],
            condition="incident.priority matches 'P1'",
            subscribed_to_all_services=False)
        devops = pagerduty.get_team(name="devops")
        manual_trigger = pagerduty.IncidentWorkflowTrigger("manualTrigger",
            type="manual",
            workflow=my_first_workflow.id,
            services=[pagerduty_service["first_service"]["id"]])
        ```

        ## Import

        Incident workflows can be imported using the `id`, e.g.

        ```sh
         $ pulumi import pagerduty:index/incidentWorkflowTrigger:IncidentWorkflowTrigger pagerduty_incident_workflow_trigger PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param IncidentWorkflowTriggerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IncidentWorkflowTriggerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[str]] = None,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subscribed_to_all_services: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IncidentWorkflowTriggerArgs.__new__(IncidentWorkflowTriggerArgs)

            __props__.__dict__["condition"] = condition
            __props__.__dict__["services"] = services
            if subscribed_to_all_services is None and not opts.urn:
                raise TypeError("Missing required property 'subscribed_to_all_services'")
            __props__.__dict__["subscribed_to_all_services"] = subscribed_to_all_services
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            if workflow is None and not opts.urn:
                raise TypeError("Missing required property 'workflow'")
            __props__.__dict__["workflow"] = workflow
        super(IncidentWorkflowTrigger, __self__).__init__(
            'pagerduty:index/incidentWorkflowTrigger:IncidentWorkflowTrigger',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[str]] = None,
            services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            subscribed_to_all_services: Optional[pulumi.Input[bool]] = None,
            type: Optional[pulumi.Input[str]] = None,
            workflow: Optional[pulumi.Input[str]] = None) -> 'IncidentWorkflowTrigger':
        """
        Get an existing IncidentWorkflowTrigger resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] condition: A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        :param pulumi.Input[bool] subscribed_to_all_services: Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        :param pulumi.Input[str] type: [Updating causes resource replacement] May be either `manual` or `conditional`.
        :param pulumi.Input[str] workflow: The workflow ID for the workflow to trigger.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IncidentWorkflowTriggerState.__new__(_IncidentWorkflowTriggerState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["services"] = services
        __props__.__dict__["subscribed_to_all_services"] = subscribed_to_all_services
        __props__.__dict__["type"] = type
        __props__.__dict__["workflow"] = workflow
        return IncidentWorkflowTrigger(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional[str]]:
        """
        A [PCL](https://developer.pagerduty.com/docs/ZG9jOjM1NTE0MDc0-pcl-overview) condition string which must be satisfied for the trigger to fire.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def services(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of service IDs. Incidents in any of the listed services are eligible to fire this trigger.
        """
        return pulumi.get(self, "services")

    @property
    @pulumi.getter(name="subscribedToAllServices")
    def subscribed_to_all_services(self) -> pulumi.Output[bool]:
        """
        Set to `true` if the trigger should be eligible for firing on all services. Only allowed to be `true` if the services list is not defined or empty.
        """
        return pulumi.get(self, "subscribed_to_all_services")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        [Updating causes resource replacement] May be either `manual` or `conditional`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def workflow(self) -> pulumi.Output[str]:
        """
        The workflow ID for the workflow to trigger.
        """
        return pulumi.get(self, "workflow")

