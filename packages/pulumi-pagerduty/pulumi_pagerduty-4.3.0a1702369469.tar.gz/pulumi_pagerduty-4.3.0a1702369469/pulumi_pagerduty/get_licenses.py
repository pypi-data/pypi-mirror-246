# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetLicensesResult',
    'AwaitableGetLicensesResult',
    'get_licenses',
    'get_licenses_output',
]

@pulumi.output_type
class GetLicensesResult:
    """
    A collection of values returned by getLicenses.
    """
    def __init__(__self__, id=None, licenses=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if licenses and not isinstance(licenses, list):
            raise TypeError("Expected argument 'licenses' to be a list")
        pulumi.set(__self__, "licenses", licenses)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        ID of the license
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def licenses(self) -> Sequence['outputs.GetLicensesLicenseResult']:
        """
        The list of purchased licenses.
        """
        return pulumi.get(self, "licenses")


class AwaitableGetLicensesResult(GetLicensesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLicensesResult(
            id=self.id,
            licenses=self.licenses)


def get_licenses(id: Optional[str] = None,
                 licenses: Optional[Sequence[pulumi.InputType['GetLicensesLicenseArgs']]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLicensesResult:
    """
    Use this data source to get information about the purchased [licenses](https://developer.pagerduty.com/api-reference/4c10cb38f7381-list-licenses) that you can use for other managing PagerDuty user resources. To reference a unique license, see `get_license` [data source](https://registry.terraform.io/providers/PagerDuty/pagerduty/latest/docs/data-sources/pagerduty_license). After applying changes to users' licenses, the `current_value` and `allocations_available` attributes of licenses will change.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    invalid_roles = ["owner"]
    licenses = pagerduty.get_licenses()
    example = pagerduty.User("example",
        email="125.greenholt.earline@graham.name",
        license=licenses.licenses[0].id,
        role="user")
    ```


    :param str id: Allows to override the default behavior for setting the `id` attribute that is required for data sources.
    :param Sequence[pulumi.InputType['GetLicensesLicenseArgs']] licenses: The list of purchased licenses.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['licenses'] = licenses
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('pagerduty:index/getLicenses:getLicenses', __args__, opts=opts, typ=GetLicensesResult).value

    return AwaitableGetLicensesResult(
        id=pulumi.get(__ret__, 'id'),
        licenses=pulumi.get(__ret__, 'licenses'))


@_utilities.lift_output_func(get_licenses)
def get_licenses_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                        licenses: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetLicensesLicenseArgs']]]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLicensesResult]:
    """
    Use this data source to get information about the purchased [licenses](https://developer.pagerduty.com/api-reference/4c10cb38f7381-list-licenses) that you can use for other managing PagerDuty user resources. To reference a unique license, see `get_license` [data source](https://registry.terraform.io/providers/PagerDuty/pagerduty/latest/docs/data-sources/pagerduty_license). After applying changes to users' licenses, the `current_value` and `allocations_available` attributes of licenses will change.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    invalid_roles = ["owner"]
    licenses = pagerduty.get_licenses()
    example = pagerduty.User("example",
        email="125.greenholt.earline@graham.name",
        license=licenses.licenses[0].id,
        role="user")
    ```


    :param str id: Allows to override the default behavior for setting the `id` attribute that is required for data sources.
    :param Sequence[pulumi.InputType['GetLicensesLicenseArgs']] licenses: The list of purchased licenses.
    """
    ...
