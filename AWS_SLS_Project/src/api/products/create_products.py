import json
import uuid

from common.repository import DynamoDBRepository


def lambda_handler(event, context):
    """Create a product in the Products DynamoDB table."""

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
            "body": json.dumps({"message": "Request body must contain product data."})
        }

    product_id = payload.get("productId") or str(uuid.uuid4())
    item = {**payload, "productId": product_id}

    repo = DynamoDBRepository("Products")
    repo.create_item(item)

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(item)
    }
