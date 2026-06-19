from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, firebase_uid, email, **extra_fields):
        if not firebase_uid:
            raise ValueError("firebase_uid is required")
        email = self.normalize_email(email)
        user = self.model(firebase_uid=firebase_uid, email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, firebase_uid, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(firebase_uid, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CONSUMER = "consumer", "Consumer"
        STORE_STAFF = "store_staff", "Store Staff"

    firebase_uid = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    username = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    photo_url = models.URLField(blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CONSUMER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "firebase_uid"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email
