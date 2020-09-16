from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all()), UnicodeUsernameValidator])
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        token, _ = Token.objects.get_or_create(user=obj)
        attr.__setitem__('token', token.key)
        return attr

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', )


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        token, _ = Token.objects.get_or_create(user=obj)
        attr.__setitem__('token', token.key)
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User not exist")
        if not User.objects.get(username=username).check_password(password):
            raise serializers.ValidationError("Invalid Credential")
        return attrs

    def create(self, validated_data):
        return User.objects.get(username=validated_data.get('username'))

    class Meta:
        model = User
        fields = ('username', 'password', )
