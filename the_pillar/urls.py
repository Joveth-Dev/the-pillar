"""the_pillar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from djoser import views as djoser_views

admin.site.site_header = 'THE PILLAR'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('userprofile/', include('userprofile.urls')),
    path('publication/', include('publication.urls')),
    # path('university/', include('university.urls')),
    # path('playground/', include('playground.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),

    # for sending emial for forgot password feature
    # to customize templates for this endpoints the template_name inside as_view() should be called
    # path('reset_password/', auth_views.PasswordResetView.as_view(),
    #      name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
