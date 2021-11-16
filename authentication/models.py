from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
       Custom users model manager where email and mobile is the unique identifiers
       for authentication instead of usernames.
       """

    def create_user(self,employee_num, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        # extra_fields.setdefault('auth_provider', 'SYSTEM')
        # if not email:
        #     raise ValueError(_('The Email must be set'))
        if not employee_num:
            raise ValueError(_('The employee_num must be set'))

        # email = self.normalize_email(email)
        user = self.model(employee_num=employee_num, **extra_fields)
        user.set_password(password)
        # user.mobile = mobile
        user.save()
        return user

    def create_superuser(self, employee_num, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault('auth_provider', 'SYSTEM')
        extra_fields.setdefault('role', self.model.ADMIN)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
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
    employee_num = models.CharField(max_length=4,unique=True)
    is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # unique_string = models.CharField(max_length=255, unique=True)
    # mail_confirmed = models.BooleanField(default=False)
    # auth_provider = models.CharField(max_length=50, choices=auth_provider_choices, default=SYSTEM, blank=False,
    #                                  null=False)
    # app_provider = models.CharField(max_length=50, choices=app_provider_choices, default=YOURPARTS)
    # birth_date = models.DateField(null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'employee_num'
    # REQUIRED_FIELDS = ['employee_num']

    def __str__(self):
        return (self.employee_num )

    # def save(self, *args, **kwargs):
    #     if self.is_superuser :
    #         self.unique_string = self.email
    #     elif self.email and self.mobile:
    #         self.unique_string = f'{self.email}-{str(self.mobile)}'
    #     elif self.email:
    #         self.unique_string = f'{self.email}'
    #     else:
    #         self.unique_string = f'{str(uuid.uuid4())}'
    #     super(User, self).save(*args, **kwargs)
    #
    # def set_favorite_car(self, car_id):
    #     user_cars = self.user_cars_related.all()
    #     selected_car = get_object_or_404(user_cars, car_id=car_id)
    #     user_cars.update(is_favorite=False)
    #     selected_car.is_favorite = True
    #     selected_car.save()
