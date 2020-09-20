from django.urls import path, include
from . import views
from knox.views import LogoutView, LogoutAllView
from .api import *

urlpatterns = [
    path('home/',views.index),
    path('api/auth/',include("knox.urls")),
    path('api/auth/register',RegistrationAPI.as_view()),
    path('api/auth/login',LoginAPI.as_view()),
    path('api/auth/add_teacher',TeacherAPI.as_view()),
    path('api/auth/logout',LogoutView.as_view()),
    path('api/auth/logoutall',LogoutAllView.as_view()),
    path('api/school/accounts/<str:t_first>_<str:t_last>',views.SchoolView.as_view()),
    path('api/school/teachers/<str:t_name>',views.TeacherView.as_view()),
    path('api/school/teachers_login',TeacherLoginAPI.as_view()),
    path('api/school/students/addsession',StudentAddSession.as_view()),
    path('api/school/students/addframe',FrameAPI.as_view()),
    path('api/school/entry',SchoolAPI.as_view()),
    path('api/school/emotions/<str:t_first>_<str:t_last>',views.AverageEmotionView.as_view()),
    path('api/school/teachers_addsession',AddSession.as_view()),
    path('api/school/frames/<str:t_first>_<str:t_last>',views.RealTimeFrameView.as_view()),
]