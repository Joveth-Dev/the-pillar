from django.contrib.auth.models import AbstractUser
from django.db import models
from . validators import validate_image_size


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='core/images',
        null=True,
        blank=True,
        validators=[validate_image_size])
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

    def save(self, *args, **kwargs):
        if self.avatar == '':
            if self.profile.sex == 'M':
                self.avatar == 'core/images/default_male.jpg'
            if self.profile.sex == 'F':
                self.avatar == 'core/images/default_female.jpg'
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # set is_active to False instead of deleting
        self.is_active = False
        super(User, self).save(*args, **kwargs)
