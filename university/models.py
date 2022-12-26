from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from userprofile.models import Profile


class College(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class DegreeProgram(models.Model):
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name='degreeprograms')
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Student(models.Model):
    student_id = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(000000),
                    MaxValueValidator(999999,
                    "Ensure this is exactly 6 digits.")],
        null=True,
        blank=True)
    college = models.ForeignKey(
        College,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    degree_program = models.ForeignKey(
        DegreeProgram,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.user.get_full_name()


class StudentPulse(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='studentpulses')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
