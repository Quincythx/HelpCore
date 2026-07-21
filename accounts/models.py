from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, employee_id, password=None, **extra_fields):
        if not employee_id:
            raise ValueError("Users must have an employee_id")
        user = self.model(employee_id=employee_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(employee_id, password, **extra_fields)


class User(AbstractUser):
    username = None
    employee_id = models.CharField(max_length=20, unique=True)

    class Role(models.TextChoices):
        EMPLOYEE = "employee", "Employee"
        IT_STAFF = "it_staff", "IT Staff"
        ADMIN = "admin", "Admin"

    class Department(models.TextChoices):
        FINANCE = "finance", "Finance"
        OPERATIONS = "operations", "Operations"
        IT = "it", "IT"
        HR = "hr", "Human Resources"
        SALES = "sales", "Sales"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )
    department = models.CharField(
        max_length=20,
        choices=Department.choices,
        default=Department.IT,
    )

    USERNAME_FIELD = "employee_id"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.employee_id} ({self.get_role_display()})"