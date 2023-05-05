from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nip = models.CharField(
        verbose_name="NIP",
        help_text=_("Nomor Induk Pegawai"),
        max_length=225,
        unique=True,
    )
    email = models.EmailField(verbose_name="Email", db_index=True)
    username = models.CharField(
        verbose_name="Username", max_length=225, default="username"
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "nip"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "account_user"
