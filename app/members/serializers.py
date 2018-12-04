from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_pk = serializers.CharField(source='pk')

    class Meta:
        model = User
        fields = (
            'user_pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'img_profile',
        )


class SiteSigunUpSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def to_internal_value(self, data):

        # Perform the data validation. username/password
        if not data.get('username'):
            raise serializers.ValidationError({
                'username': 'This field is required.'
            })
        if not data.get('password'):
            raise serializers.ValidationError({
                'password': 'This field is required.'
            })

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({
                '중복': '이미 존재하는 ID로 회원가입을 시도합니다'
            })

        filtered_data = {
            'username': data.get('username'),
            'password': data.get('password'),
        }

        # 추가 사항이 있는 경우 data에 추가하기
        extra_fields = ['first_name', 'last_name', 'email', 'img_profile']

        for field in extra_fields:
            if data.get(field):
                filtered_data[field] = data.get(field)

        self.user = User.objects.create_user(**filtered_data)

        return filtered_data

    def to_representation(self, instance):

        return UserSerializer(self.user).data


class SiteAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('아이디 또는 비밀번호가 올바르지 않습니다')
        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data


class SocialAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def to_internal_value(self, data):
        if not data.get('username'):
            raise serializers.ValidationError({
                'username': 'This field is required.'
            })

        filtered_data = {}

        extra_fields = ['username', 'first_name', 'last_name', 'email', 'img_profile']

        for field in extra_fields:
            if data.get(field):
                filtered_data[field] = data.get(field)

        try:
            user = User.objects.get(username=filtered_data['username'])
        except User.DoesNotExist:
            user = User.objects.create_user(**filtered_data)

        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data
