from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser precisa precisa estar como True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff precisa precisa estar como True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=150)
    is_staff = models.BooleanField('Equipe', default=False)
    is_instructor = models.BooleanField('Instrutor', default=False)
    objects = UserManager()
    # social
    job = models.CharField(max_length=100)
    bio = models.TextField()
    site = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email

    def first_name(self):
        return self.name.split(' ')[0]

    def get_url_profile(self):
        first_name = self.name.split(' ')[0]
        last_name = None
        if len(self.name.split(' ')) > 1:
            last_name = self.name.split(' ')[1]
        if last_name:
            return f'https://ui-avatars.com/api/?name={first_name}+{last_name}&background=000&color=fff&format=png'
        return f'https://ui-avatars.com/api/?name={first_name}&background=000&color=fff&format=png'
