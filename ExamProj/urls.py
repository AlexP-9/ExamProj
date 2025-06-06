"""
URL configuration for ExamProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include

import AdventureApp, AdventureApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("adventures/",include("AdventureApp.urls")),
    path("",lambda request: redirect("adventures/")),

    path("accounts/login/",AdventureApp.views.view_login, name="login"),
    path("accounts/logout/",AdventureApp.views.view_logout, name="logout"),
    path("accounts/registration/",AdventureApp.views.view_register, name="registration"),
    path("accounts/editdata/",AdventureApp.views.view_account_edit_data,name="edit_user_data"),
    path("accounts/newpassword/",AdventureApp.views.view_account_new_password,name="new_password"),
]

#A workaround so that we don't have to serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
