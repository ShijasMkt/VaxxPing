from django.urls import path
from .views import *

urlpatterns = [
    path('',loginPage,name='login'),
    path('dashboard',dashboardView,name='dashboard'),
    path('logout',logoutView,name='logout'),
    path('add_patient', add_patient, name='add_patient'),
    path('add_vaccine',add_vaccine,name="add_vaccine"),
    path("schedule_vaccine",schedule_vaccine,name="schedule_vaccine"),
    path("view_schedules",view_schedules,name="view_schedules"),
    path("send_reminder",send_vaccine_reminders,name="send_reminder")

]