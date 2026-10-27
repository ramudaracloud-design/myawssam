from __future__ import annotations

import boto3
from boto3.resources.base import ServiceResource

# Created once and reused by Lambda execution environment
_dynamodb_resource: ServiceResource | None = None


def get_dynamodb() -> ServiceResource:
    """
    Returns a singleton DynamoDB resource.

    This is Lambda-friendly because the resource is reused across warm
    invocations.
    """
    global _dynamodb_resource

    if _dynamodb_resource is None:
        _dynamodb_resource = boto3.resource("dynamodb")

    return _dynamodb_resource