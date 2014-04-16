from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save

class Profile(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    initial_weight = models.FloatField()
    height = models.FloatField()
    # Relations
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')


class CheckPoint(models.Model):
    date = models.DateField()
    is_planned = models.BooleanField()
    weight = models.FloatField()
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checkpoints')


class Mentor(models.Model):
    email = models.EmailField(max_length=150)
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mentors')


class CustomuserManager(BaseUserManager):
    """
    Create superuser
    """
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        if password is None:
            raise ValueError('Users must have an password')

        user = self.model(
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password = password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomuserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

