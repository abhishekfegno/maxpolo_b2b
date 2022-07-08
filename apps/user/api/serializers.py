from rest_framework import serializers

from apps.user.models import User, Complaint, Banners, Dealer, SiteConfiguration


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    class Meta:
        fields = ('username', 'password')


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
    zone = serializers.SerializerMethodField()

    def get_zone(self, instance):
        return instance.zone and instance.zone.name

    class Meta:
        model = Dealer
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'user_role', 'zone', 'company_cin',
                  'address_street', 'address_city', 'address_state')


class DealerDetailSerializer(serializers.ModelSerializer):
    zone = serializers.SerializerMethodField()

    def get_zone(self, instance):
        return instance.zone and instance.zone.name

    class Meta:
        model = Dealer
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'user_role', 'zone', 'company_cin',
                  'address_street', 'address_city', 'address_state')


class ExcalationNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = ('excalation_number',)
