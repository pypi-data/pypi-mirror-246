from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 404  # or whatever you want
    default_code = '404'
    #  Custom response below
    default_detail = {"code": 404, "message": "item_not_exists"}
