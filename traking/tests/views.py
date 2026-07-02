from rest_framework.views import APIView
from rest_framework.request import Request 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from traking.mixins import LoggingMixin


class MockWithoutMixinAPIView(APIView):
    def get(self, request: Request) -> Response:
        return Response("logg does not exist!")
    

class MockWithMixinAPIView(LoggingMixin, APIView):
    def get(self, request: Request) -> Response:
        return Response("logg does exist")
    

class MockExplicitLoggingView(LoggingMixin, APIView):
    logging_methods = ["POST"]

    def get(self, request):
        return Response("no logging")
    
    def post(self, request):
        return Response("with logging")


class MockCustomCheckLoggingView(LoggingMixin, APIView):
    def should_log(self, request: Request, response: Response) ->bool:
        return 'log' in response.data
    
    def get(self, request: Request)->Response:
        return Response('with logging')
    
    def post(self, request: Request) -> Response:
        return Response("no recording")
    

class MockSessionAuthLoggingView(LoggingMixin, APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication,)

    def get(self, request: Request) -> Response:
        return Response('with session auth logging')
    
class MockTokenAuthLoggingView(LoggingMixin, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response('with token auth logging')
    

class MockSensitiveFieldsLoggingView(LoggingMixin, APIView):
    sensetive_fields = {'mY_fiEld'}

    def get(self, request: Request) -> Response:
        return Response('with loggin ')
    

class MockInvalidCleanedSubstituteLoggingView(LoggingMixin, APIView):
    CLEANED_SUBSTITUTE = 1 