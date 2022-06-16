import os
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.gis.db import models

from apps.user.models import Dealer, Executive


class Zone(models.Model):
    name = models.CharField(max_length=128)
    reverser = 'district'
    branch_filter = 'branch'

    def __str__(self):
        return f'{self.name}'

#
# class Lead(models.Model):
#     """
#     Store model maps every entry, a sales executive gets
#     """
#     reverser = 'lead'
#     name = models.CharField(max_length=128, help_text="Name of the store")
#     address = models.TextField(null=True, help_text="Place")
#     mobile = PhoneNumberField(null=True)
#     place = models.CharField(max_length=32, null=True, help_text="District", verbose_name="Place")
#     dealer_account = models.ForeignKey('user.Dealer', on_delete=models.SET_NULL, null=True, blank=True,
#                                        help_text="Dealer Account, for this lead, if lead is registered as a Dealer")
#     executive = models.ForeignKey('user.Executive', on_delete=models.CASCADE,
#                                   help_text="The Executive, to whom this Store is assigned to")
#     location = models.PointField(null=True, blank=True)
#     is_removed = models.BooleanField(default=False)
#     shared_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
#     DEALER = 'Dealer'
#     LEAD = 'Lead'
#     PROJECT = 'Project'
#     lead_type = models.CharField(max_length=12, default='Lead', choices=[
#         (LEAD, LEAD), (DEALER, DEALER), (PROJECT, PROJECT)
#     ])
#
#     class Meta:
#         unique_together = [['dealer_account', 'executive']]
#
#     def convert(self):
#         if self.dealer_account is None:
#             from apps.user.models import Dealer
#             dealer, _ = Dealer.objects.get_or_create(
#                 mobile=self.mobile,
#                 defaults={
#                     'name': self.name,
#                     "branch": self.executive.branch,
#                     "address": self.address,
#                     "place": self.place,
#                     # "state": getattr(self, 'state') if hasattr(self, 'state') else None,
#                 }
#             )
#             dealer.executive.add(self)
#             self.lead_type = Lead.DEALER
#             self.save()

#
# class CheckInDay(models.Model):
#     check_in_at = models.DateTimeField()
#     location = models.PointField(null=True)
#     location_text = models.TextField(null=True, blank=True)
#     device_name = models.TextField(null=True, blank=True)
#     device_id = models.TextField(null=True, blank=True)
#     battery_percentage = models.IntegerField(null=True, blank=True)
#     executive = models.ForeignKey('user.Executive', on_delete=models.CASCADE,
#                                   help_text="The Executive, who is getting logged into")
#
#     template_name = 'executivetracking/utils/checkinday-template.html'
#
#     @property
#     def as_html(self):
#         return render_to_string('executivetracking/utils/checkinday-template.html', {'point': self})
#
#     def __str__(self):
#         return f'{self.executive.name}  checked in at {self.check_in_at.date()} by {self.check_in_at.time()}'
#


class CheckPoint(models.Model):
    store = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='checked_points')
    executive = models.ForeignKey(Executive, on_delete=models.CASCADE, related_name='checkpoints')
    check_in_at = models.DateTimeField()
    check_out_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.PointField(null=True)
    file = models.FileField(upload_to='executive-check-point-recordings/', null=True, blank=True)
    location_text = models.TextField(null=True, blank=True)
    device_name = models.TextField(null=True, blank=True)
    device_id = models.TextField(null=True, blank=True)
    battery_percentage = models.IntegerField(null=True, blank=True)

    template_name = 'executivetracking/utils/checkpoint-template.html'

    @property
    def as_html(self):
        return render_to_string('executivetracking/utils/checkpoint-template.html', {'point': self})

    @property
    def distance(self):
        return self.store.location.distance(self.location)

    @property
    def file_extension(self):
        name, extension = os.path.splitext(self.file.name)
        return f'audio/{extension.replace(".", "")}'

    @property
    def time_diff(self):
        from django.utils import timezone
        now = timezone.now()
        time_diff = 0
        if not self.check_out_at and self.check_in_at < now:
            time_diff = (now - self.check_in_at).seconds / 60

        elif self.check_in_at < self.check_out_at:
            time_diff = (self.check_out_at - self.check_in_at).seconds // 60
        out = ''
        hours = time_diff // 60
        if hours:
            out += f"{hours} Hours, "
        return out + f"{int(int(time_diff % 60) // 1) } minutes.  "


class CrashReport(models.Model):
    device_name = models.CharField(max_length=64, null=True, blank=True)
    error_string = models.TextField(null=True, blank=True)
    stack_trace = models.TextField(null=True, blank=True)
    other_information = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return f'{self.created_at} > {self.device_name} > {self.other_information}'


