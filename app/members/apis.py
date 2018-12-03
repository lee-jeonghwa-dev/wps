from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SiteAuthTokenSerializer, SocialAuthTokenSerializer
from .serializers import UserSerializer

User = get_user_model()


class SignUpCheckIDView(APIView):
    def post(self, request, format=None):
        username = request.POST.get('user_id')
        if not username:
            data = {'error': 'user_id 값이 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        user_exist = User.objects.filter(username=username).exists()
        if user_exist:
            # 같은 ID가 존재함
            data = {'error': '동일한 ID가 존재합니다'}
        else:
            data = {'pass': '사용가능한 ID입니다'}
        return Response(data, status=status.HTTP_200_OK)


class SiteSignUpAPIView(APIView):
    def post(self, request, format=None):
        username = request.POST.get('user_id')
        password = request.POST.get('password')

        if not (username and password):
            data = {'error': 'user_id 또는 password값이 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            # 같은 ID가 존재함
            data = {'error': '동일한 ID가 존재합니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response(
            data=UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


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
