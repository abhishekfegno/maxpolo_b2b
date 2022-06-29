from rest_framework import serializers

from apps.executivetracking.models import CheckPoint, CrashReport


# CheckInDay,


# class LeadSerializer(serializers.ModelSerializer):
#     location = GeometryField()
#
#     class Meta:
#         model = Lead
#         fields = (
#             "id", "name", "address", "mobile", "place", "location", "dealer_account",
#         )

# def save(self, **kwargs):
#     user = self.context['request'].user
#     if user.is_authenticated and user.user_role == user.EXECUTIVE:
#         kwargs.update({'executive': user.account})
#     return super(LeadSerializer, self).save(**kwargs)


class CrashReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrashReport
        fields = '__all__'


class CheckPointSerializer(serializers.ModelSerializer):
    # location = GeometryField()
    # store = LeadSerializer()
    check_in_type = serializers.SerializerMethodField()

    def get_check_in_type(self, instance):
        return 'check-point'

    # def validate_store(self, store):
    #     if store not in Lead.objects.filter(executive__user=self.context['request'].user):
    #         raise serializers.ValidationError("The lead you are selected is not assigned to you!")
    #     return store

    class Meta:
        model = CheckPoint
        fields = (
            'id', "store", "executive", "check_in_at", "check_out_at", "description",
            "file", "location_text", "device_name", "device_id", 'check_in_type',
            'battery_percentage'
        )


class CheckPointReadSerializer(CheckPointSerializer):
    # store = LeadSerializer()

    class Meta:
        model = CheckPoint
        fields = (
            'id', "store", "check_in_at", "check_out_at", "description", "location",
            "file", "location_text", "device_name", "device_id", 'check_in_type',
            'battery_percentage'
        )

#
# class CheckInDaySerializer(serializers.ModelSerializer):
#     location = PointField()
#     check_in_type = serializers.SerializerMethodField()
#     store = serializers.SerializerMethodField()
#
#     def get_store(self, instance):
#         return None
#
#     def get_check_in_type(self, instance):
#         return 'check-in-day'
#
#     class Meta:
#         model = CheckInDay
#         fields = (
#             'id', "check_in_at", "location", "location_text",
#             "device_name", "device_id", 'check_in_type', 'battery_percentage', 'store'
#         )
#
#     def save(self, **kwargs):
#         user = self.context['request'].user
#         if user.is_authenticated and user.user_role == user.EXECUTIVE:
#             kwargs.update({'executive': user.account})
#         return super(CheckInDaySerializer, self).save(**kwargs)
#
#
