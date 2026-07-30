from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import uuid
from django.utils import timezone
from datetime import timedelta
import random



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
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "employee_id"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_user = User.objects.order_by('-id').first()
            next_number = (last_user.id + 1) if last_user else 1
            self.employee_id = f"EMP{next_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} ({self.get_role_display()})"



class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification_token")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        expiry_time = self.created_at + timedelta(hours=2)
        return timezone.now() < expiry_time

class LoginOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_otps")
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time and not self.is_used

    @staticmethod
    def generate_code():
        return str(random.randint(10000, 99999))