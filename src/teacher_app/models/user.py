from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from teacher_app.models.base import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, verbose_name="user name", unique=True)
    first_name = models.CharField(max_length=100, verbose_name="user name")
    last_name = models.CharField(max_length=100, verbose_name="user surname")
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User #{self.pk} {self.first_name} {self.last_name}"

    USERNAME_FIELD = "username"
    manager = UserManager()
    objects = manager


class Student(BaseModel):
    first_name = models.CharField(max_length=100, verbose_name="user name")
    last_name = models.CharField(max_length=100, verbose_name="user surname")
    patronymic = models.CharField(
        max_length=100, verbose_name="user patronymic", null=True, blank=True
    )
    group = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}, {self.group}"
