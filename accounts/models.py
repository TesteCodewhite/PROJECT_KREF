# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        SCHOOL = 'SCHOOL', 'Escola'
        TEACHER = 'TEACHER', 'Professor'
        STUDENT = 'STUDENT', 'Aluno'

    role = models.CharField(max_length=50, choices=Role.choices)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')
    # Adicionar outros campos específicos do Admin, se necessário
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class SchoolProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='school_profile')
    school_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school_name

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile')
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='teachers')
    # subjects = models.ManyToManyField('core.Subject', blank=True) # Assumindo um app 'core' para Subject
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='students')
    date_of_birth = models.DateField(null=True, blank=True)
    series = models.CharField(max_length=50, blank=True, null=True) # Campo adicionado
    turma = models.CharField(max_length=50, blank=True, null=True)  # Campo adicionado
    # classrooms = models.ManyToManyField('core.Classroom', blank=True) # Assumindo um app 'core' para Classroom
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

