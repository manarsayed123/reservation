from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
       Custom users model manager where email and mobile is the unique identifiers
       for authentication instead of usernames.
       """

    def create_user(self, employee_num, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not employee_num:
            raise ValueError('The employee_num must be set')
        user = self.model(employee_num=employee_num, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, employee_num, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.ADMIN)
        return self.create_user(employee_num, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = "Admin"
    EMPLOYEE = "Employee"
    role_choices = (
        (ADMIN, ADMIN),
        (EMPLOYEE, EMPLOYEE),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=role_choices)
    is_superuser = models.BooleanField(default=False)
    employee_num = models.CharField(max_length=4, unique=True, validators=[MinLengthValidator(4)], )
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'employee_num'

    def __str__(self):
        return (self.employee_num)
