from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .validators import validate_image_size


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NOT_SET = 'N'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NOT_SET, 'Not set'),
    ]
    birth_date = models.DateField(
        null=True,
        blank=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=SEX_CHOICES[2][0])
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    state_or_province = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    zip_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        max_length=4)
    country = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='profile')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.middle_initial}. {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    # def save(self, *args, **kwargs):
    #     if self.user.avatar == '':
    #         if self.sex == 'N':
    #             self.user.avatar = 'core/images/default_no_sex.jpg'
    #         if self.sex == 'M':
    #             self.user.avatar = 'core/images/default_male.jpg'
    #         if self.sex == 'F':
    #             self.user.avatar = 'core/images/default_female.jpg'
    #     super(Profile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
