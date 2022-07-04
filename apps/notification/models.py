from django.db import models

# Create your models here.


class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
