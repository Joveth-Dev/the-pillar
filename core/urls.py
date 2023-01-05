from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path

# URLConf
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html')),
    path('confirm_reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/password_reset_done.html'),
         name='password_reset_complete'),
]
