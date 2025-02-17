import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Missions(models.Model):
    name = models.CharField(max_length=255)
    launch_details = models.JSONField()
    landing_details = models.JSONField()
    spacecraft = models.JSONField()


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, patronymic, password=None, birth_date=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
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



# Модель пользователя
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Пароль будет хэшироваться через set_password
    birth_date = models.DateField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Дополнительные поля, которые могут быть полезны


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'patronymic', 'birth_date']

    objects = UserManager()

