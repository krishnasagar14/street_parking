# _*_ coding: utf-8 _*_

import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model - customized model for user data storage and authentication driver model
    for application authorization services.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, \
                          db_index=True)
    email = models.EmailField('Email Address', unique=True, blank=False)
    first_name = models.CharField('First Name', max_length=100, blank=False)
    last_name = models.CharField('Last Name', max_length=100, blank=False)
    date_joined = models.DateTimeField('Joining Date', auto_now_add=True)
    is_active = models.BooleanField('Is User Active', default=True)
    mobile_no = models.CharField('Mobile Number', max_length=12, blank=True)
    is_staff = models.BooleanField('Staff User', default=False)
    is_superuser = models.BooleanField('Super User', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        db_table = 'Users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        """
        Derives and return full name of user using first and last name.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()