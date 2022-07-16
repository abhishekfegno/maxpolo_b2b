from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.executivetracking.models import Zone
from apps.infrastructure.models import Branch
from apps.user.models import User, Complaint, Banners, Dealer, SiteConfiguration


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    class Meta:
        fields = ('username', 'password')


class ProfileAPISerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    zone = serializers.SerializerMethodField()

    def get_branch(self, instance):
        if instance.branch:
            return instance.branch.name

    def get_zone(self, instance):
        if instance.zone:
            return instance.zone.name

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile', 'branch', 'company_cin',
                  'address_street', 'address_city', 'address_state', 'zone')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)

    class Meta:
        fields = ('email', )


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=10)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs.get('password') == attrs.get('confirm_password'):
            return super().validate(attrs)
        else:
            raise ValidationError("Password doesn't match !!")

    class Meta:
        fields = ('password', 'confirm_password')


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
    username = serializers.SerializerMethodField()

    def get_zone(self, instance):
        return instance.zone and instance.zone.name

    class Meta:
        model = Dealer
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'user_role', 'zone', 'company_cin',
                  'address_street', 'address_city', 'address_state')

nce = SalesOrder.objects.create(dealer=validated_data[
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


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'