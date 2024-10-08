from rest_framework import status
from rest_framework.response import Response
from .serializers import GoogleSignInSerializer, GithubOauthSerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class GoogleSignInView(GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = ((serializer.validated_data)['access_token'])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GithubSignInView(GenericAPIView):
    serializer_class = GithubOauthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = ((serializer.validated_data)['code'])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)