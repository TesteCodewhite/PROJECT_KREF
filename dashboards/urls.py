# dashboards/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("redirect/", views.dashboard_redirect, name="dashboard_redirect"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("school/", views.school_dashboard, name="school_dashboard"),
    path("school/upload-students/", views.upload_students_excel, name="upload_students_excel"), # Rota para o upload
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("access-denied/", views.access_denied, name="access_denied"),
]

