'''
[![npm version](https://badge.fury.io/js/demo-awscdk-construct.svg)](https://badge.fury.io/js/demo-awscdk-construct)
[![PyPI version](https://badge.fury.io/py/demo-awscdk-construct.svg)](https://badge.fury.io/py/demo-awscdk-construct)
[![release](https://github.com/hustshawn/my-ecs-quickstart-construct/actions/workflows/release.yml/badge.svg)](https://github.com/hustshawn/my-ecs-quickstart-construct/actions/workflows/release.yml)

# ECS Construct Quickstart

This is a sample project to use projen to create CDK Construct and publish to registries like `npm` and `pypi`.

## Usage

```python
    const app = new cdk.App();
    const stack = new cdk.Stack(app, "MyStack");
    new MyEcs(stack, "MyEcs");
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class MyEcs(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="demo-awscdk-construct.MyEcs",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b3c382136d235b3608be3f38145fad80ec9ddba03ae0ac03087790872f14fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MyEcsProps(vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))


@jsii.data_type(
    jsii_type="demo-awscdk-construct.MyEcsProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class MyEcsProps:
    def __init__(
        self,
        *,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param vpc: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5602a9dfb8194ba57c3270e4c782438df1766349dd54cca7483e1b5928546a0)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MyEcsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MyEcs",
    "MyEcsProps",
]

publication.publish()

def _typecheckingstub__91b3c382136d235b3608be3f38145fad80ec9ddba03ae0ac03087790872f14fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5602a9dfb8194ba57c3270e4c782438df1766349dd54cca7483e1b5928546a0(
    *,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
