from rest_framework import serializers

from apps.user.models import User, Complaint, Banners, Dealer


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    class Meta:
        fields = ('email', 'password')


class ProfileAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile', 'branch', 'company_cin',
                  'address_street', 'address_city', 'address_state', 'zone')


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=50)

    class Meta:
        fields = ('username', 'email')


class ComplaintSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('id', 'title', 'photo', 'ticket_id', 'description', 'status',  'is_public', 'created_at', 'created_by', 'order_id')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'username', 'user_role', 'branch')
