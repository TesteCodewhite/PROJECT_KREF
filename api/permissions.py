# api/permissions.py

from rest_framework import permissions
from accounts.models import User

class IsAdminUser(permissions.BasePermission):
    """Permite acesso apenas a usuários Admin."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsSchoolUser(permissions.BasePermission):
    """Permite acesso apenas a usuários Escola."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.SCHOOL

class IsTeacherUser(permissions.BasePermission):
    """Permite acesso apenas a usuários Professor."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.TEACHER

class IsStudentUser(permissions.BasePermission):
    """Permite acesso apenas a usuários Aluno."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.STUDENT

class IsAdminOrReadOnly(permissions.BasePermission):
    """Permite acesso total a Admins, ou apenas leitura para outros autenticados."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsAdminOrSchoolOrReadOnly(permissions.BasePermission):
    """Permite acesso total a Admins/Escolas, ou apenas leitura para outros autenticados."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.ADMIN or request.user.role == User.Role.SCHOOL)

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Permite acesso total ao dono do objeto ou Admin, ou leitura para outros."""
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer requisição,
        # então sempre permitimos GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permissões de escrita são permitidas apenas para o dono do perfil ou admin.
        # Assumindo que o objeto tem um campo 'user'
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.role == User.Role.ADMIN
        # Se o objeto for o próprio User
        elif isinstance(obj, User):
            return obj == request.user or request.user.role == User.Role.ADMIN
        return False

class IsSchoolOwnerOrAdmin(permissions.BasePermission):
    """Permite acesso ao Admin ou à Escola dona do perfil (Professor/Aluno)."""
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer requisição autenticada (ajustar se necessário)
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Permissões de escrita
        if not (request.user and request.user.is_authenticated):
            return False

        # Admin tem acesso total
        if request.user.role == User.Role.ADMIN:
            return True

        # Escola pode modificar perfis associados a ela
        if request.user.role == User.Role.SCHOOL:
            # Verifica se o perfil (obj) pertence à escola (request.user.schoolprofile)
            if hasattr(obj, 'school') and obj.school == request.user.schoolprofile:
                return True
            # Se o obj for um User (Aluno/Professor), verifica se o perfil associado pertence à escola
            elif isinstance(obj, User) and obj.role in [User.Role.TEACHER, User.Role.STUDENT]:
                profile = getattr(obj, 'teacherprofile', None) or getattr(obj, 'studentprofile', None)
                return profile and profile.school == request.user.schoolprofile

        return False

