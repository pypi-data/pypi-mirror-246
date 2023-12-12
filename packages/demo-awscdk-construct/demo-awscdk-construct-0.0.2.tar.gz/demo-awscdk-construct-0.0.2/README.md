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
