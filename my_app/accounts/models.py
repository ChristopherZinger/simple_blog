from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.utils.text import slugify
import datetime
import random
import re
import string


class MyUserManager(BaseUserManager):
    def create_unique_slug(self):
        random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
        slug = make_password('{}-{}'.format(datetime.datetime.now(),random_string))
        slug = slugify(slug)[22:]
        user = User.objects.filter(slug=slug)
        if user.exists():
            return create_slug(instance)
        return slug


    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        #create and check slug
        slug = self.create_unique_slug()
        if slug == None: return None

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            slug=slug,
        )
        user.active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    slug=models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField( default=True,)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField( default=False, )
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_active(self):
    #     "Is the user a member of active?"
    #     # Simplest possible answer: All admins are staff
    #     return self.active

    @property
    def is_admin(self):
        "Is the user a member of admin?"
        # Simplest possible answer: All admins are staff
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.staff


class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='user_info', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email



def create_slug(instance):
    random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    slug = make_password('{}-{}'.format(datetime.datetime.now(),random_string))
    slug = slugify(slug)[22:]
    user = User.objects.filter(slug=slug)
    if user.exists():
        return create_slug(instance)
    return slug


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_slug, User)
