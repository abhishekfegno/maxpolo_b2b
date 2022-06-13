from rest_framework import serializers

from apps.catalogue.models import Product
from apps.user.models import User, Complaint


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    class Meta:
        fields = ('username', 'password')


class ProfileAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile', 'branch')


class ComplaintSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
