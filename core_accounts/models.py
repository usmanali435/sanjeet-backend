import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from core_accounts.manager import CustomUserManager



class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("Patient", "Patient"),
        ("Doctor", "Doctor"),
    )
    _id = models.CharField(max_length=100, db_index=True, null=True, unique=True, default="")
    profile_url = models.ImageField(upload_to="profile/images", db_index=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    username = models.CharField(max_length=300, null=True, db_index=True, blank=True)
    bio = models.TextField(db_index=True, null=True)
    email = models.EmailField(null=False, unique=True, db_index=True)
    otp = models.PositiveIntegerField(null=True, db_index=True)
    otp_limit = models.IntegerField(null=True, db_index=True)
    otp_delay = models.TimeField(auto_now=True, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    last_login = models.DateTimeField(default=None, null=True, db_index=True)
    is_blocked = models.BooleanField(default=False, null=True, db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    is_staff = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='', null=True, db_index=True)
    password = models.CharField(max_length=200, db_index=True, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    users_messaging_container = models.ManyToManyField('self', symmetrical=False)

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self._id:
            unique_str = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            self._id = f'bud-{unique_str}'
        print(f"Saving user with _id: {self._id}")  # Log _id generation
        super(User, self).save(*args, **kwargs)
