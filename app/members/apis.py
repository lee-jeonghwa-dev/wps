from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SiteAuthTokenSerializer, SocialAuthTokenSerializer

User = get_user_model()


class SiteSignUpAPIView(APIView):
    def post(self, request, data):
        pass


class SiteAuthTokenAPIView(APIView):
    def post(self, request, format=None):
        serializer = SiteAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthTokenAPIView(APIView):

    def post(self, request, format=None):
        serializer = SocialAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
