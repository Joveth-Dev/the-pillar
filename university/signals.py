# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from userprofile.models import Profile
# from .models import Student


# @receiver(post_save, sender=Profile)
# def create_student_for_new_profile(sender, **kwargs):
#     if kwargs['created']:
#         profile = kwargs['instance']
#         if profile.is_student:
#             Student.objects.create(profile=kwargs['instance'])
