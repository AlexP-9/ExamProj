"""
URL configuration for BlogProj project.

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
from django.urls import path
from . import views

urlpatterns = [
    path("",views.view_mainpage,name="main_page"),
    path("trips/", views.view_all_trips, name="view_all_trips"),
    path("trip/<int:tid>/",views.view_trip,name="trip"),
    path("trip/<int:tid>/schedules",views.view_trip_full_schedule,name="trip_full_schedule"),
    #path("trip/",views.,name="trips"),  #Do we need this one?
    path("trips/register/<int:sid>", views.view_trip_register, name="trip_register"),
    path("trips/register/<int:sid>/confirm", views.view_trip_register_confirm, name="trip_register_confirm"),

    path("profile/",views.view_profile,name="profile"),
    path("profile/history/",views.view_trip_history,name="trip_history"),

    path("about/",views.view_about,name="about"),
    path("contact/",views.view_contact,name="contact"),

    #path("login/",views.view_login,name="login"),
    #path("register/",views.view_register,name="login"),
    #path("logout/",views.view_logout,name="logout"),

    path("manage/",views.view_managing_panel,name="managing_panel"),
    path("manage/schedule/",views.view_schedule,name="manage_schedule"),
    path("manage/schedule/add",views.view_schedule_add,name="man_schedule_add"),
    path("manage/schedule/edit/<int:sched_id>",views.view_schedule_edit,name="man_schedule_edit"),
    path("manage/schedule/delete/<int:sched_id>",views.view_schedule_delete,name="man_schedule_delete"),
    path("manage/schedule/delete/<int:sched_id>/confirm",views.view_schedule_delete_conf,name="man_schedule_delete_conf"),
    path("trip/add/",views.view_add_trip,name="add_trip"),

    path("debug/",views.view_debug,name="debug"),
]
