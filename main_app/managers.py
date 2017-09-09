# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, first_name, last_name, group_number, mobile_phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            group_number=group_number,
            mobile_phone=mobile_phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, group_number, mobile_phone, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            group_number=group_number,
            mobile_phone=mobile_phone
        )
        user.is_admin = True

        user.save(using=self._db)
        return user
