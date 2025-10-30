from django.db.models import BaseUserManager

from rides.models import Roles


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, role=Roles.RIDER, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, role=role, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('role', 'admin')

        return self.create_user(*args, **kwargs)
