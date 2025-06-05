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
from . import views_managing

urlpatterns = [
    path("",views.view_mainpage,name="main_page"),
    path("trips/", views.view_all_trips, name="view_all_trips"),
    path("trip/<int:tid>/",views.view_trip,name="trip"),
    path("trip/<int:tid>/schedules",views.view_trip_full_schedule,name="trip_full_schedule"),
    path("trips/register/<int:sid>", views.view_trip_register, name="trip_register"),
    path("trips/register/<int:sid>/confirm", views.view_trip_register_confirm, name="trip_register_confirm"),

    path("profile/",views.view_profile,name="profile"),
    path("profile/history/",views.view_trip_history,name="trip_history"),

    path("about/",views.view_about,name="about"),

    path("manage/",views_managing.view_managing_panel,name="managing_panel"),

    path("manage/trips/",views_managing.view_trip_list,name="manage_trips"),
    path("manage/trip/add/",views_managing.view_trip_add,name="trip_add"),
    path("manage/trip/<int:tid>/",views_managing.view_trip_edit,name="trip_edit"),
    path("manage/trip/<int:tid>/pictures/",views_managing.view_trip_manage_pics,name="trip_man_pics"),
    path("manage/trip/<int:tid>/delete/",views_managing.view_trip_delete,name="trip_delete"),
    path("manage/trip/<int:tid>/delete/confirm/",views_managing.view_trip_delete_confirm,name="trip_delete_confirm"),

    path("manage/pictures/<int:pid>/delete/",views_managing.view_pic_delete,name="man_pic_delete"),
    path("manage/pictures/<int:pid>/delete/confirm/",views_managing.view_pic_delete_confirm,name="man_pic_delete_confirm"),

    path("manage/schedule/",views_managing.view_schedule_list,name="manage_schedule"),
    path("manage/schedule/add/",views_managing.view_schedule_add,name="man_schedule_add"),
    path("manage/schedule/<int:sched_id>",views_managing.view_schedule_edit,name="man_schedule_edit"),
    path("manage/schedule/<int:sched_id>/delete/",views_managing.view_schedule_delete,name="man_schedule_delete"),
    path("manage/schedule/<int:sched_id>/delete/confirm/",views_managing.view_schedule_delete_conf,name="man_schedule_delete_conf"),

    path("manage/guides/",views_managing.view_guide_list,name="manage_guides"),
    path("manage/guide/add/",views_managing.view_guide_add,name="guide_add"),
    path("manage/guide/<int:gid>/",views_managing.view_guide_edit,name="guide_edit"),
    path("manage/guide/<int:gid>/delete/",views_managing.view_guide_delete,name="guide_delete"),
    path("manage/guide/<int:gid>/delete/confirm/",views_managing.view_guide_delete_confirm,name="guide_delete_confirm"),


    #path("debug/",views.view_debug,name="debug"),
]
