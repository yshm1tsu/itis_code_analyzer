from django.urls import path

from teacher_app.views import add_student_view, manage_configuration_statistics

urlpatterns = [
    path("add_student/", add_student_view, name="form"),
    path("statistics/", manage_configuration_statistics, name="statistics"),
]
