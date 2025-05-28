# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Cria um router para registrar os ViewSets automaticamente
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'schools', views.SchoolProfileViewSet, basename='schoolprofile')
router.register(r'teachers', views.TeacherProfileViewSet, basename='teacherprofile')
router.register(r'students', views.StudentProfileViewSet, basename='studentprofile')
# Registrar outros ViewSets aqui (atividades, métricas, etc.)

# As URLs da API são determinadas automaticamente pelo router.
urlpatterns = [
    path('', include(router.urls)),
    # Adiciona URLs de login/logout para a API browsable do DRF
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]

