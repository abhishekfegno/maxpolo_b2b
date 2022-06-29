from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from solo.models import SingletonModel


# Create your models here.
from lib.faker import FakeImage
from lib.sent_email import EmailHandler


class Role:
    ADMIN_STR = 'Admin'

    WAREHOUSE_MANAGER_STR = 'Warehouse Manager'
    BRANCH_MANAGER_STR = 'Branch Manager'

    EXECUTIVE_STR = 'Executive'
    DEALER_STR = 'Dealer'

    RECEPTIONIST_STR = 'Receptionist'

    ADMIN = 1
    BRANCH_MANAGER = 2
    WAREHOUSE_MANAGER = 4
    RECEPTIONIST = 8

    EXECUTIVE = 16
    DEALER = 32
    DEFAULT = 100
    FIELD_FORCE_MANAGER = 90

    USER_ROLE_CHOICE = (
        (ADMIN, ADMIN_STR),
        (WAREHOUSE_MANAGER, WAREHOUSE_MANAGER_STR),
        (BRANCH_MANAGER, BRANCH_MANAGER_STR),
        (EXECUTIVE, EXECUTIVE_STR),
        (DEALER, DEALER_STR),
        (RECEPTIONIST, RECEPTIONIST_STR),
    )


class DealerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_role=Role.DEALER)


class ExecutiveManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_role=Role.EXECUTIVE)


class User(AbstractUser):
    chosen_role = Role.DEFAULT
    mobile = models.CharField(max_length=20)
    user_role = models.CharField(max_length=20, choices=Role.USER_ROLE_CHOICE, default=Role.EXECUTIVE, blank=True)
    branch = models.ForeignKey('infrastructure.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    executive = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dealers')

    company_cin = models.CharField(max_length=50, null=True, blank=False)
    address_street = models.CharField(max_length=50, null=True, blank=False)
    address_city = models.CharField(max_length=50, null=True, blank=False)
    address_state = models.CharField(max_length=50, null=True, blank=False)
    zone = models.ForeignKey('executivetracking.Zone', on_delete=models.SET_NULL, null=True, blank=False)

    @property
    def address(self):
        return self.get_full_name(), self.company_cin, self.address_street, self.address_street, self.address_city

    @property
    def user_role_name(self):
        if self.user_role == '32':
            return "Dealer"
        if self.user_role == '16':
            return "Executive"
        if self.user_role == '1':
            return "Admin"

    def save(self, **kwargs):
        self.user_role = self.chosen_role
        super(User, self).save(**kwargs)

    def __str__(self):
        return self.username


class Dealer(User):
    chosen_role = Role.DEALER
    objects = DealerManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.username


class Executive(User):
    chosen_role = Role.EXECUTIVE
    objects = ExecutiveManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.username


class Complaint(models.Model):
    STATUS = (
        ('new', 'New'),
        ('under processing', 'Under Processing'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )
    # ticket_id = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=False)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    order_id = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description

    @property
    def ticket_id(self):
        return 'TKT' + f'{self.pk}'.zfill(6)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Banners(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    photo = models.ImageField(upload_to='banners/', default='default/banner.jpg', null=True, blank=True)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = str(self.title).lower().replace(' ', '-')
        return super().save(*args, **kwargs)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return settings.MEDIA_URL + settings.DEFAULT_IMAGE

    def __str__(self):
        return self.title


class SiteConfiguration(SingletonModel):
    site_logo = models.ImageField(null=True)
    email_01 = models.EmailField(default='hello@fegno.com')
    email_02 = models.EmailField(default='manoj@fegno.com')
    email_03 = models.EmailField(default='jomon@fegno.com')
    email_04 = models.EmailField(default='jerinisready@gmail.com')

    @property
    def enquiry_emails(self):
        return [self.email_01, self.email_02, self.email_03, self.email_04]

    @enquiry_emails.setter
    def enquiry_emails(self, value):
        for index in range(len(value)):
            if index < 4:
                setattr(self, f'email_0{index + 1}', value[index])



@receiver(post_save, sender=Complaint)
def sent_email_complaint(sender, created, instance, **kwargs):
    if created:
        EmailHandler().sent_mail_complaint(instance)


@receiver(post_save, sender=Complaint)
def sent_email_banners(sender, created, instance, **kwargs):
    if created:
        EmailHandler().sent_mail_for_banners(instance)

