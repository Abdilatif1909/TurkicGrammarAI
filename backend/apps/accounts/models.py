from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.core.models import BaseModel


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    RESEARCHER = "RESEARCHER", "Researcher"
    STUDENT = "STUDENT", "Student"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", UserRole.STUDENT)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("role", UserRole.SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=UserRole.choices, default=UserRole.STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email

    @property
    def is_super_admin(self) -> bool:
        return self.role == UserRole.SUPER_ADMIN or self.is_superuser

    @property
    def is_researcher(self) -> bool:
        return self.role == UserRole.RESEARCHER

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    institution = models.CharField(max_length=255, blank=True)
    research_area = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["user__email"]

    def __str__(self) -> str:
        return f"Profile: {self.user.email}"
