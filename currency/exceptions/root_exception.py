from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status

class BaseException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'
    
class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('A server error occurred.')
    default_code = 'error'