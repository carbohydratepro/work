from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=False, max_length=50)
    email = models.EmailField(unique=True, null=True, default=None)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    view_type = models.CharField(max_length=5, default='mix')
    position = models.CharField(max_length=10, default="chick") #chick kitchen floor all

    store_code = models.CharField(max_length=10, null=True, default=None)
    employee_id_number = models.CharField(unique=True, max_length=20, null=True, default=None)
    objects = CustomUserManager()

    USERNAME_FIELD = 'employee_id_number'
