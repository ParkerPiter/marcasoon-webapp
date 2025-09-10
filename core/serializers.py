from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import  Trademark, TrademarkAsset


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone_number')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class TrademarkAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrademarkAsset
        fields = ('id', 'kind', 'text_value', 'logo', 'sound', 'created_at')


class TrademarkSerializer(serializers.ModelSerializer):
    assets = TrademarkAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Trademark
        fields = ('id', 'user', 'assets', 'created_at', 'updated_at')