from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError

from .client import get_dynamodb
from .exceptions import (
    DynamoDBRepositoryException,
    InvalidUpdateException,
    ItemNotFoundException,
)
from .types import Item, Key


class DynamoDBRepository:
    """
    Generic reusable DynamoDB repository.

    Works with any DynamoDB table.
    """

    def __init__(self, table_name: str, dynamodb=None):
        self._resource = dynamodb or get_dynamodb()
        self._table = self._resource.Table(table_name)

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------

    def create_item(self, item: Item) -> Item:

        try:
            self._table.put_item(Item=item)
            return item

        except ClientError as ex:
            raise DynamoDBRepositoryException(ex.response["Error"]["Message"]) from ex

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------

    def get_item(self, key: Key) -> Item:

        try:
            response = self._table.get_item(Key=key)

            item = response.get("Item")

            if item is None:
                raise ItemNotFoundException(f"Item not found: {key}")

            return item

        except ClientError as ex:
            raise DynamoDBRepositoryException(ex.response["Error"]["Message"]) from ex

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------

    def delete_item(self, key: Key) -> None:

        try:
            self._table.delete_item(Key=key)

        except ClientError as ex:
            raise DynamoDBRepositoryException(ex.response["Error"]["Message"]) from ex

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------

    def update_item(
        self,
        key: Key,
        attributes: dict[str, Any],
    ) -> Item:

        if not attributes:
            raise ItemNotFoundException("Update payload cannot be empty.")

        update_expression = []
        expression_values = {}
        expression_names = {}

        for index, (k, v) in enumerate(attributes.items()):
            name = f"#n{index}"
            value = f":v{index}"

            update_expression.append(f"{name}={value}")

            expression_names[name] = k
            expression_values[value] = v

        try:

            response = self._table.update_item(
                Key=key,
                UpdateExpression="SET " + ", ".join(update_expression),
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW",
            )

            return response["Attributes"]

        except ClientError as ex:
            raise DynamoDBRepositoryException(ex.response["Error"]["Message"]) from ex

    # ----------------------------------------------------------
    # SCAN
    # ----------------------------------------------------------

    def scan(
        self,
        filter_expression=None,
        projection_expression: str | None = None,
        limit: int | None = None,
    ) -> list[Item]:

        kwargs = {}

        if filter_expression is not None:
            kwargs["FilterExpression"] = filter_expression

        if projection_expression:
            kwargs["ProjectionExpression"] = projection_expression

        if limit:
            kwargs["Limit"] = limit

        items = []

        response = self._table.scan(**kwargs)
        items.extend(response.get("Items", []))

        while "LastEvaluatedKey" in response:

            response = self._table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"],
                **kwargs,
            )

            items.extend(response.get("Items", []))

        return items

    # ----------------------------------------------------------
    # QUERY
    # ----------------------------------------------------------

    def query(
        self,
        key_condition_expression,
        index_name: str | None = None,
        filter_expression=None,
        projection_expression: str | None = None,
    ) -> list[Item]:

        kwargs = {
            "KeyConditionExpression": key_condition_expression
        }

        if index_name:
            kwargs["IndexName"] = index_name

        if filter_expression:
            kwargs["FilterExpression"] = filter_expression

        if projection_expression:
            kwargs["ProjectionExpression"] = projection_expression

        response = self._table.query(**kwargs)

        return response.get("Items", [])