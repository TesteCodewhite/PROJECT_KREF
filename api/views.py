# api/views.py

from rest_framework import viewsets, permissions
from accounts.models import User, SchoolProfile, TeacherProfile, StudentProfile
from .serializers import UserSerializer, SchoolProfileSerializer, TeacherProfileSerializer, StudentProfileSerializer
from .permissions import IsAdminUser, IsSchoolUser, IsTeacherUser, IsStudentUser, IsOwnerOrAdminOrReadOnly, IsSchoolOwnerOrAdmin, IsAdminOrSchoolOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar e editar usuários."""
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    # Apenas Admin pode listar/criar/deletar usuários.
    # Usuário pode ver/editar seu próprio perfil (IsOwnerOrAdminOrReadOnly cuida disso).
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_permissions(self):
        # Apenas Admin pode criar usuários via API (outros criados via registro/upload)
        if self.action == 'create':
            self.permission_classes = [IsAdminUser]
        # Apenas Admin pode listar todos os usuários
        elif self.action == 'list':
             self.permission_classes = [IsAdminUser]
        # Permissão padrão (IsOwnerOrAdminOrReadOnly) para retrieve, update, partial_update, destroy
        else:
            self.permission_classes = [IsOwnerOrAdminOrReadOnly]
        return super().get_permissions()

class SchoolProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar e editar perfis de Escola."""
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileSerializer
    # Apenas Admin pode listar/criar/deletar escolas.
    # Escola pode ver/editar seu próprio perfil.
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else: # retrieve, update, partial_update
            self.permission_classes = [IsOwnerOrAdminOrReadOnly]
        return super().get_permissions()

class TeacherProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar e editar perfis de Professor."""
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    # Admin pode tudo. Escola pode listar/criar/editar/deletar professores da sua escola.
    # Professor pode ver/editar seu próprio perfil.
    permission_classes = [IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return TeacherProfile.objects.all()
        elif user.role == User.Role.SCHOOL:
            return TeacherProfile.objects.filter(school=user.schoolprofile)
        elif user.role == User.Role.TEACHER:
            return TeacherProfile.objects.filter(user=user)
        return TeacherProfile.objects.none() # Outros não veem nada

    def get_permissions(self):
        # Admin ou Escola podem criar/listar
        if self.action in ['create', 'list']:
            self.permission_classes = [IsAdminUser | IsSchoolUser]
        # Permissões de objeto (IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly) para retrieve, update, partial_update, destroy
        else:
             self.permission_classes = [IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly]
        return super().get_permissions()

class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar e editar perfis de Aluno."""
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # Admin pode tudo. Escola pode listar/criar/editar/deletar alunos da sua escola.
    # Professor pode listar alunos da sua escola (apenas leitura).
    # Aluno pode ver/editar seu próprio perfil.
    permission_classes = [IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return StudentProfile.objects.all()
        elif user.role == User.Role.SCHOOL:
            return StudentProfile.objects.filter(school=user.schoolprofile)
        elif user.role == User.Role.TEACHER:
            # Professor vê alunos da mesma escola
            if hasattr(user, 'teacherprofile'):
                 return StudentProfile.objects.filter(school=user.teacherprofile.school)
            return StudentProfile.objects.none()
        elif user.role == User.Role.STUDENT:
            return StudentProfile.objects.filter(user=user)
        return StudentProfile.objects.none()

    def get_permissions(self):
        # Admin ou Escola podem criar
        if self.action == 'create':
            self.permission_classes = [IsAdminUser | IsSchoolUser]
        # Admin, Escola ou Professor podem listar (Professor só da sua escola via get_queryset)
        elif self.action == 'list':
             self.permission_classes = [IsAdminUser | IsSchoolUser | IsTeacherUser]
        # Permissões de objeto (IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly) para retrieve, update, partial_update, destroy
        # Professor não pode editar/deletar alunos via API por padrão (apenas Admin/Escola/Próprio Aluno)
        else:
             self.permission_classes = [IsSchoolOwnerOrAdmin | IsOwnerOrAdminOrReadOnly]
        return super().get_permissions()

# Adicionar ViewSets para outros modelos (Activity, Submission, Metrics, etc.) conforme necessário,
# aplicando as permissões apropriadas.

