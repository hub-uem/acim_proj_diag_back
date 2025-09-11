from django.db import models
from localflavor.br.models import BRCNPJField
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        print("EXTRA_FIELDS:", extra_fields)
        if not email:
            raise ValueError('Usuários devem ter um endereço de email.')

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    PORTE_CHOICES = [
        ('PL', 'Profissional Liberal'),
        ('MEI', 'Mei'),
        ('EPP', 'Epp'),
        ('ME', 'Me'),
        ('MEDIA', 'Média'),
        ('GRANDE', 'Grande'),
    ]

    SETOR_CHOICES = [
        ('Comercio', 'Comercio'),
        ('Indústria', 'Industria'),
        ('Serviço', 'Servico'),
    ]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    cnpj = BRCNPJField(max_length=14, unique=True)
    porte = models.CharField(max_length=20, choices=PORTE_CHOICES, default='PL')
    setor = models.CharField(max_length=20, choices=SETOR_CHOICES, default='Comercio')

    registration_date = models.DateTimeField(default=timezone.now)
    deactivation_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'cnpj', 'porte', 'setor']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.is_active and not self.deactivation_date:
            self.deactivation_date = timezone.now()
        super().save(*args, **kwargs)
