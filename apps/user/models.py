from django.contrib.auth.models import AbstractUser
from django.db import models

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

    USER_ROLE_CHOICE = [
        (ADMIN, ADMIN_STR),
        (WAREHOUSE_MANAGER, WAREHOUSE_MANAGER_STR),
        (BRANCH_MANAGER, BRANCH_MANAGER_STR),
        (EXECUTIVE, EXECUTIVE_STR),
        (DEALER, DEALER_STR),
        (RECEPTIONIST, RECEPTIONIST_STR),
    ]


class User(AbstractUser):
    mobile = models.CharField(max_length=20)
    user_role = models.CharField(max_length=20, default=Role.EXECUTIVE)
    branch = models.ForeignKey('infrastructure.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    dealers = models.ManyToManyField('self', null=True, blank=True)

    @property
    def user_role_name(self):
        if self.user_role == 16:
            return Role.EXECUTIVE
        if self.user_role == 32:
            return Role.DEALER
        if self.user_role == 1:
            return Role.ADMIN

    def __str__(self):
        return self.username


class Dealer(User):
    chosen_role = Role.DEALER

    class Meta:
        proxy = True

    def __str__(self):
        return self.username


class Executive(User):
    chosen_role = Role.EXECUTIVE

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
