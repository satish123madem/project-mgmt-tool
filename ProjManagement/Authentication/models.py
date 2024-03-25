from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    role = models.CharField(max_length=30)
    description = models.TextField()


class User(AbstractUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=True)
    no_of_logins = models.BigIntegerField(default=0, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserLogins(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    login_time = models.DateTimeField(auto_now=True, null=False)
    login_status = models.BooleanField()
    payload = models.TextField(null=True)

    def __str__(self) -> str:
        return self.user.email + f" -- {self.login_status} "
