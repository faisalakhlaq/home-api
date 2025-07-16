from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_409_CONFLICT


class DuplicateFavoriteError(APIException):
    status_code = HTTP_409_CONFLICT
    default_detail = "This property is already in favorites."
    default_code = "duplicate_favorite"
