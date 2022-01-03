from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
  """UserManager Model"""

  def create_user(self, email, name, password=None):
    """Create new user"""

    if not email:
      raise  ValueError('User must have an email address')

    email = self.normalize_email(email)
    user = self.model(email=email, name=name)

    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, email, name, password):
    """Create new super user"""

    user = self.create_user(email, name, password)

    user.is_superuser = True
    user.is_staff = True

    user.save(using=self._db)

    return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
  """User Model"""

  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def get_full_name(self):
    """Get user full name"""

    return self.name

  def get_short_name(self):
    """Get user short name"""

    return self.name

  def __str__(self):
    """Convert object to string"""

    return self.email


class ProfileFeedItem(models.Model):
  """Profile status update"""

  user_profile = models.ForeignKey('User', on_delete=models.CASCADE)
  status_text = models.CharField(max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    """Return the model as a string"""

    return self.status_text
