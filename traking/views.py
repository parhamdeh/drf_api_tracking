from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .mixins import LoggingMixin


class HomeAPIView(LoggingMixin, APIView):
    def get(self, request: Request) -> Response:
        return Response("hello", status=status.HTTP_200_OK)
