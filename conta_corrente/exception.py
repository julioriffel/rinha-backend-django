
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):

    data = {'detail': str(exc)}

    if isinstance(exc, ValidationError):
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif isinstance(exc, IntegrityError):
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return exception_handler(exc, context)
