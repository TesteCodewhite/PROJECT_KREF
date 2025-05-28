# dashboards/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.dateparse import parse_date
from accounts.models import User, SchoolProfile, TeacherProfile, StudentProfile
from .forms import ExcelUploadForm
import pandas as pd
import random
import re # Para limpar CPF

# Decorator para verificar o tipo de usuário
def role_required(allowed_roles=[]):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return render(request, "dashboards/access_denied.html")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@login_required
def dashboard_redirect(request):
    if request.user.role == User.Role.ADMIN:
        return redirect("admin_dashboard")
    elif request.user.role == User.Role.SCHOOL:
        return redirect("school_dashboard")
    elif request.user.role == User.Role.TEACHER:
        return redirect("teacher_dashboard")
    elif request.user.role == User.Role.STUDENT:
        return redirect("student_dashboard")
    else:
        # Redirecionamento padrão ou página de erro
        return redirect("login")

@role_required(allowed_roles=[User.Role.ADMIN])
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")

@role_required(allowed_roles=[User.Role.SCHOOL])
def school_dashboard(request):
    try:
        school_profile = request.user.schoolprofile
    except SchoolProfile.DoesNotExist:
        # Tratar caso o perfil não exista (embora não devesse acontecer para usuário SCHOOL)
        messages.error(request, "Perfil da escola não encontrado.")
        return redirect("login") # Ou outra página apropriada

    upload_form = ExcelUploadForm()
    context = {
        "school_profile": school_profile,
        "upload_form": upload_form,
    }
    return render(request, "dashboards/school_dashboard.html", context)

@role_required(allowed_roles=[User.Role.TEACHER])
def teacher_dashboard(request):
    try:
        teacher_profile = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        messages.error(request, "Perfil do professor não encontrado.")
        return redirect("login")
    context = {"teacher_profile": teacher_profile}
    return render(request, "dashboards/teacher_dashboard.html", context)

@role_required(allowed_roles=[User.Role.STUDENT])
def student_dashboard(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Perfil do aluno não encontrado.")
        return redirect("login")
    context = {"student_profile": student_profile}
    return render(request, "dashboards/student_dashboard.html", context)

# --- Upload de Alunos via Excel --- #

@role_required(allowed_roles=[User.Role.SCHOOL])
@transaction.atomic # Garante que ou todos os alunos são criados ou nenhum
def upload_students_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            try:
                df = pd.read_excel(excel_file)
                required_columns = ["aluno", "série", "turma", "data_nacimento (DD/MM/AAAA)", "cpf (apenas números)", "email_escolar"]
                if not all(col in df.columns for col in required_columns):
                    messages.error(request, f"O arquivo Excel deve conter as colunas: {', '.join(required_columns)}")
                    return redirect("school_dashboard")

                school_profile = request.user.schoolprofile
                success_count = 0
                error_list = []
                special_chars = ["_", "*", "%", "#", "!"]

                for index, row in df.iterrows():
                    try:
                        # Extração e Limpeza de Dados
                        full_name = str(row["aluno"]).strip()
                        series = str(row["série"]).strip()
                        turma = str(row["turma"]).strip()
                        dob_str = str(row["data_nacimento (DD/MM/AAAA)"]).strip()
                        cpf = str(row["cpf (apenas números)"]).strip()
                        cpf = re.sub(r'\D+', '', cpf) # Remove não-dígitos
                        school_email = str(row["email_escolar"]).strip()

                        # Validações Básicas
                        if not all([full_name, series, turma, dob_str, cpf, school_email]):
                            raise ValueError(f"Linha {index + 2}: Dados incompletos.")
                        if len(cpf) != 11:
                            raise ValueError(f"Linha {index + 2}: CPF inválido ({cpf}). Deve ter 11 dígitos.")
                        try:
                            dob = parse_date(dob_str) # Tenta parsear como AAAA-MM-DD
                            if not dob:
                                # Tenta parsear como DD/MM/AAAA
                                parts = dob_str.split("/")
                                if len(parts) == 3:
                                    dob = parse_date(f"{parts[2]}-{parts[1]}-{parts[0]}")
                            if not dob:
                                raise ValueError("Formato de data inválido")
                        except ValueError:
                             raise ValueError(f"Linha {index + 2}: Data de nascimento inválida ({dob_str}). Use DD/MM/AAAA.")

                        # Geração de Credenciais
                        first_name = full_name.split(" ")[0].lower()
                        last_3_cpf = cpf[-3:]
                        username = f"{first_name}{last_3_cpf}" # Ex: joao123
                        site_email = f"{username}@sefice.com.br"
                        password_name_part = re.sub(r'\s+', '', full_name).lower()
                        password_dob_part = dob.strftime("%d%m%Y")
                        password_special_char = random.choice(special_chars)
                        password = f"{password_name_part}{password_special_char}{password_dob_part}"

                        # Verifica se usuário/email já existe
                        if User.objects.filter(username=username).exists():
                             raise ValueError(f"Linha {index + 2}: Nome de usuário '{username}' já existe.")
                        if User.objects.filter(email=site_email).exists():
                             raise ValueError(f"Linha {index + 2}: Email '{site_email}' já existe.")

                        # Criação do Usuário e Perfil
                        user = User.objects.create_user(
                            username=username,
                            email=site_email,
                            password=password,
                            role=User.Role.STUDENT,
                            first_name=full_name.split(" ")[0],
                            last_name=" ".join(full_name.split(" ")[1:])
                        )
                        StudentProfile.objects.create(
                            user=user,
                            school=school_profile,
                            date_of_birth=dob,
                            # Adicionar série e turma se forem campos no modelo StudentProfile
                            series=series, # Descomentado
                            turma=turma    # Descomentado
                        )
                        success_count += 1

                    except Exception as e:
                        error_list.append(f"Erro na linha {index + 2}: {e}")

                # Feedback Final
                if success_count > 0:
                    messages.success(request, f"{success_count} alunos registrados com sucesso.")
                if error_list:
                    for error in error_list:
                        messages.error(request, error)
                    messages.warning(request, "Alguns alunos não puderam ser registrados. Verifique os erros acima e corrija o arquivo.")
                else:
                     messages.info(request, "Todos os alunos do arquivo foram processados.")

            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo Excel: {e}")
        else:
            messages.error(request, "Erro no formulário. Por favor, selecione um arquivo .xlsx válido.")
    else:
        # Se for GET, apenas redireciona de volta, pois a view principal já mostra o form
        pass

    return redirect("school_dashboard")




@login_required
def access_denied(request):
    """View para exibir a página de acesso negado."""
    return render(request, "dashboards/access_denied.html")

