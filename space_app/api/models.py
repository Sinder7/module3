import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, patronymic, birth_date, password=None):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            birth_date=birth_date
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email =  models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    birth_date =models.DateField()
    password = models.CharField(max_length=100)
    token = models.UUIDField(default=uuid.uuid4(), editable=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "patronymic", "birth_date", "password"]

    object = UserManager()



class Mission(models.Model):
    name = models.CharField(max_length=255)
    launch_details = models.JSONField()
    landing_details = models.JSONField()
    spacecraft = models.JSONField()
