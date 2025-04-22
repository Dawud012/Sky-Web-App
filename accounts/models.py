from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class StaffManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Staff(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

