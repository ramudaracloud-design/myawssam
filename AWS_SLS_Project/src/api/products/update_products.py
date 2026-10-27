import json

from common.repository import DynamoDBRepository


def lambda_handler(event, context):
    """Update a product in the Products DynamoDB table."""

    path_parameters = event.get("pathParameters") or {}
    product_id = path_parameters.get("productId")

    if not product_id:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Missing productId path parameter."})
        }

    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Invalid JSON body."})
        }

    if not isinstance(payload, dict) or not payload:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Request body must contain update data."})
        }

    payload.pop("productId", None)

    if not payload:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "No updatable fields provided."})
        }

    repo = DynamoDBRepository("Products")
    updated_item = repo.update_item({"productId": product_id}, payload)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(updated_item)
    }
