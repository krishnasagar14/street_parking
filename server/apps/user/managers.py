from django.contrib.auth.base_user import BaseUserManager

# Reference: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/
class UserManager(BaseUserManager):
    """
    Custom user manager for two types of users creation process - application's target users and admin.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **other_fields):
        """
        Creates, saves user record with given email and SHA256 hashed password
        :param email: email id in string type
        :param password: raw password text in string type
        :param other_fields: keyword arguments of extra fields
        :return: user queryset
        """
        if not email:
            raise ValueError('No email found')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **other_fields)

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **other_fields)