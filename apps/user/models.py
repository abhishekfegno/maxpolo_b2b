from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from solo.models import SingletonModel

# Create your models here.


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
    mobile = models.CharField(max_length=20)
    user_role = models.CharField(max_length=20, choices=Role.USER_ROLE_CHOICE, default=Role.EXECUTIVE, blank=True)
    branch = models.ForeignKey('infrastructure.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    dealers = models.ManyToManyField('self', null=True, blank=True)

    company_cin = models.CharField(max_length=50, null=True, blank=False)
    address_street = models.CharField(max_length=50, null=True, blank=False)
    address_city = models.CharField(max_length=50, null=True, blank=False)
    address_state = models.CharField(max_length=50, null=True, blank=False)
    zone = models.ForeignKey('executivetracking.Zone', on_delete=models.SET_NULL, null=True, blank=False)


    @property
    def user_role_name(self):
        if self.user_role == '16':
            return "Executive"
        if self.user_role == '32':
            return "Dealer"

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
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.description


class Banners(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    photo = models.ImageField(null=True, blank=True)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = str(self.title).lower().replace(' ', '-')
        return super().save(*args, **kwargs)

    @property
    def photo_url(self):
        return self.photo.url or None

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