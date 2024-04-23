from django.urls import re_path
from . import views

urlpatterns = [
    re_path("login/", views.Login.as_view(), name="login"),
    re_path("get_courses/", views.GetCourses.as_view(), name="get_courses"),
]
