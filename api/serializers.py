# api/serializers.py

from rest_framework import serializers
from accounts.models import User, SchoolProfile, TeacherProfile, StudentProfile

class UserSerializer(serializers.ModelSerializer):
    # Para evitar expor a senha hash, não a incluímos por padrão.
    # Se necessário criar/atualizar usuários via API, precisará de tratamento especial.
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "role_display", "is_active"]
        read_only_fields = ["id", "role_display"]

class SchoolProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Aninhado para visualização
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.SCHOOL),
        source="user",
        write_only=True
    )

    class Meta:
        model = SchoolProfile
        fields = ["user", "user_id", "school_name", "address", "contact_info", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.TEACHER),
        source="user",
        write_only=True
    )
    school = SchoolProfileSerializer(read_only=True) # Aninhado para visualização
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolProfile.objects.all(),
        source="school",
        write_only=True
    )

    class Meta:
        model = TeacherProfile
        fields = ["user", "user_id", "school", "school_id", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.STUDENT),
        source="user",
        write_only=True
    )
    school = SchoolProfileSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolProfile.objects.all(),
        source="school",
        write_only=True
    )

    class Meta:
        model = StudentProfile
        fields = ["user", "user_id", "school", "school_id", "date_of_birth", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

# Adicionar serializers para outros modelos (Activity, Submission, Metrics, etc.) conforme necessário.

