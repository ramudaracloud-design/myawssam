import json

from common.repository import DynamoDBRepository


def lambda_handler(event, context):
    """Delete a product from the Products DynamoDB table."""

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

    repo = DynamoDBRepository("Products")
    repo.delete_item({"productId": product_id})

    return {
        "statusCode": 204,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": ""
    }
