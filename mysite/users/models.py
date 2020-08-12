from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Please enter an email address")
        if not username:
            raise ValueError("Please enter a username")
        user = self.model(
            email = self.normalize_email(email),
            password = password,
            username=username
        )
        user.set_password(password)
        user.save(user=self._db)
        return user
    def create_superuser(self, email, username, password):
        superuser = self.model(
            email = self.normalize_email(email),
            password=password,
            username=username
        )
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser

class Account(AbstractBaseUser):
    #Required fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField("Account", blank=True, symmetrical=False, related_name="people_followers")
    following = models.ManyToManyField("Account", blank=True, symmetrical=False, related_name="people_following")
    USERNAME_FIELD = 'email' #allows user to login with email instead of username/id
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin #they have permissions if they are admin

    def has_module_perms(self, app_Label):
        return True
    @property
    def return_followers(self):
        return list(self.followers.all())

    @property
    def return_following(self):
        return list(self.following.all())