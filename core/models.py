from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_initial = models.CharField(
        max_length=1,
        default='',
        null=True,
        blank=True)
    email = models.EmailField(unique=True)

    def get_full_name(self) -> str:
        if self.middle_initial == None:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.middle_initial}. {self.last_name}'

    def delete(self, *args, **kwargs):
        # set is_active to False instead of deleting
        self.is_active = False
        super(User, self).save(*args, **kwargs)
