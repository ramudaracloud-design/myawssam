class DynamoDBRepositoryException(Exception):
    """Base repository exception."""


class ItemNotFoundException(DynamoDBRepositoryException):
    """Item not found."""


class InvalidUpdateException(DynamoDBRepositoryException):
    """Invalid update payload."""