from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class BusinessLogicError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error_code: str, message: str, details: dict = None):
        self.detail = {
            'error': error_code,
            'message': message,
            'details': details or {},
        }


class NotFoundError(BusinessLogicError):
    status_code = status.HTTP_404_NOT_FOUND


class ForbiddenError(BusinessLogicError):
    status_code = status.HTTP_403_FORBIDDEN


class ConflictError(BusinessLogicError):
    status_code = status.HTTP_409_CONFLICT


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, BusinessLogicError):
            return Response(exc.detail, status=exc.status_code)

        error_data = {
            'error': 'VALIDATION_ERROR',
            'message': 'Ошибка валидации данных',
            'details': response.data,
        }
        response.data = error_data

    return response
