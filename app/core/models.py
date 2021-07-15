from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    """Manager Class to create user"""
    # password = None for inactive user, extra fields for additional fields
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        # create a new user model
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # password has to be encrypted and we have a helper function for it
        user.set_password(password)
        user.save(using=self._db)  # support for multiple databases

        return user  # returns the user model created

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True  # from PermissionsMixin class
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email instead of username"""
    # models is imported from django.db
    email = models.EmailField(max_length=255, unique=True)  # unique user with email
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    # by default USERNAME_FIELD is username, we replacing 'username' with 'email'
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # user is going to be a foreign key to user object.
    # But instead of referencing the user object directly from above class
    # use best practice method of retrieving the auth user model setting from Django settings.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # when user is removed, remove tag as well
    )

    def __str__(self):
        """String representation of model"""
        return self.name
