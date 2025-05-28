# Plataforma Educacional Django

Este projeto é uma aplicação web desenvolvida com Django que implementa uma plataforma educacional com múltiplos níveis de acesso e dashboards personalizados para cada perfil de usuário.

## Funcionalidades Principais

*   **Quatro Níveis de Acesso:** Administrador, Escola, Professor e Aluno.
*   **Autenticação Customizada:** Sistema de login e gerenciamento de usuários com papéis definidos.
*   **Dashboards Personalizados:** Cada perfil possui um dashboard inicial com links para funcionalidades específicas (a serem implementadas).
*   **Estrutura Modular:** Organizado em apps (`accounts`, `dashboards`) para facilitar a manutenção e expansão.
*   **Pronto para Expansão:** A estrutura permite a adição de funcionalidades como gerenciamento de turmas, atividades, métricas e integração com Machine Learning.

## Estrutura do Projeto

```
/home/ubuntu/django_project/
├── educa_platform/         # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/               # App para gerenciamento de usuários e perfis
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── dashboards/             # App para os dashboards de cada perfil
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── dashboards/
│   │   ├── admin_dashboard.html
│   │   ├── school_dashboard.html
│   │   ├── teacher_dashboard.html
│   │   ├── student_dashboard.html
│   │   └── access_denied.html
│   └── registration/
│       └── login.html
├── venv/                   # Ambiente virtual Python
├── manage.py               # Utilitário de gerenciamento do Django
├── requirements.txt        # Dependências Python do projeto
├── db.sqlite3              # Banco de dados SQLite (desenvolvimento)
└── README.md               # Este arquivo
```

## Pré-requisitos

*   Python 3.10 ou superior
*   `pip` (gerenciador de pacotes Python)
*   `venv` (para criar ambientes virtuais)

## Instalação Local

1.  **Clonar o repositório (ou descompactar o projeto):**
    ```bash
    # Se fosse um repositório git:
    # git clone <url_do_repositorio>
    # cd django_project
    # Neste caso, assumindo que você já tem a pasta django_project:
    cd /home/ubuntu/django_project
    ```

2.  **Criar e ativar o ambiente virtual:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```
    *No Windows, use `venv\Scripts\activate`*

3.  **Instalar as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Criar um superusuário (Administrador):**
    ```bash
    python manage.py createsuperuser
    ```
    *Siga as instruções para definir nome de usuário, email e senha. Certifique-se de definir o `role` como `ADMIN` se solicitado ou edite via shell/admin posteriormente se o comando padrão não incluir o campo `role`.*
    *Alternativamente, o usuário `admin` com senha `adminpassword` já foi criado programaticamente nos passos anteriores.*

## Executando o Servidor de Desenvolvimento

1.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```
2.  **Acesse a aplicação:** Abra seu navegador e vá para `http://127.0.0.1:8000/` ou `http://localhost:8000/`.
3.  **Login:** Use as credenciais do superusuário criado (`admin`/`adminpassword`) ou crie outros usuários através da interface admin (`/admin/`) ou programaticamente.

## Criação de Outros Usuários (Exemplo)

Para testar os diferentes dashboards, você precisará criar usuários com os papéis correspondentes (`SCHOOL`, `TEACHER`, `STUDENT`). Isso pode ser feito:

*   **Via Django Admin:** Acesse `http://127.0.0.1:8000/admin/`, faça login como superusuário, vá para a seção "Accounts" -> "Users" e crie novos usuários, definindo o campo `Role` apropriado. Você também precisará criar os perfis correspondentes (SchoolProfile, TeacherProfile, StudentProfile) e associá-los aos usuários.
*   **Via Shell do Django:**
    ```bash
    python manage.py shell
    ```
    ```python
    from accounts.models import User, SchoolProfile, TeacherProfile, StudentProfile

    # Criar usuário Escola
    school_user = User.objects.create_user('escola1', 'escola1@example.com', 'password', role='SCHOOL')
    school_profile = SchoolProfile.objects.create(user=school_user, school_name='Escola Exemplo 1')

    # Criar usuário Professor (associado à escola criada)
    teacher_user = User.objects.create_user('prof1', 'prof1@example.com', 'password', role='TEACHER')
    teacher_profile = TeacherProfile.objects.create(user=teacher_user, school=school_profile)

    # Criar usuário Aluno (associado à escola criada)
    student_user = User.objects.create_user('aluno1', 'aluno1@example.com', 'password', role='STUDENT')
    student_profile = StudentProfile.objects.create(user=student_user, school=school_profile)

    exit()
    ```

## Implantação (Diretrizes Gerais)

Para colocar a aplicação na web, você precisará de um ambiente de hospedagem que suporte Python/Django. Algumas etapas comuns incluem:

1.  **Escolher um Provedor de Hospedagem:** Render, Heroku, Railway (mencionados no documento original), PythonAnywhere, AWS, Google Cloud, DigitalOcean, etc.
2.  **Banco de Dados:** Configurar um banco de dados de produção (PostgreSQL é recomendado para Django, mas outros como MySQL também funcionam). Atualize a seção `DATABASES` em `settings.py` para usar as credenciais do banco de dados de produção (use variáveis de ambiente!).
3.  **Servidor WSGI:** Usar um servidor WSGI como Gunicorn ou uWSGI para servir a aplicação Django.
    ```bash
    # Exemplo de instalação do Gunicorn
    pip install gunicorn
    ```
4.  **Arquivos Estáticos:** Configurar o Django para coletar e servir arquivos estáticos (CSS, JS, imagens). Use `python manage.py collectstatic` e configure um servidor web (como Nginx) ou um serviço de armazenamento (como AWS S3) para servir esses arquivos.
5.  **Variáveis de Ambiente:** **NUNCA** coloque segredos (SECRET_KEY, senhas de banco de dados, chaves de API) diretamente no código. Use variáveis de ambiente ou um sistema de gerenciamento de segredos.
6.  **Configurações de Produção:** Ajustar `settings.py` para produção:
    *   `DEBUG = False`
    *   `ALLOWED_HOSTS = ['seu_dominio.com', 'www.seu_dominio.com']`
    *   Configurar logging.
    *   Configurar email para envio de notificações ou recuperação de senha.
7.  **Segurança:** Configurar HTTPS, verificar outras configurações de segurança do Django (`check --deploy`).
8.  **Processo de Deploy:** Geralmente envolve enviar o código para o servidor (via Git, FTP, etc.), instalar dependências, aplicar migrações e iniciar/reiniciar o servidor WSGI.

*Consulte a documentação específica do seu provedor de hospedagem para obter instruções detalhadas.* 

## Pesquisa sobre Machine Learning (Solicitado)

Conforme solicitado, foi realizada uma pesquisa inicial sobre a aplicação de Machine Learning (ML) no contexto educacional para auxiliar professores:

*   **Adaptação de Atividades:** Modelos de recomendação podem sugerir atividades com base no histórico de desempenho do aluno, nível de dificuldade percebido (tempo gasto, erros) e perfil de aprendizado.
*   **Detecção de Dificuldades:** Modelos de classificação ou clustering podem identificar padrões que indicam dificuldades específicas (ex: erros recorrentes em certos tipos de problemas, alta taxa de abandono, respostas impulsivas), alertando o professor.
*   **Análise de Engajamento:** Modelos preditivos podem analisar métricas de interação (tempo na plataforma, frequência de uso, horários de pico) para prever o risco de desengajamento ou identificar os melhores momentos para estudo.
*   **Feedback Automatizado:** Processamento de Linguagem Natural (PLN) pode ser usado para analisar respostas abertas e fornecer feedback inicial ou categorizar tipos de erro.

**Próximos Passos (Sugestão):** Para integrar ML, seria necessário coletar dados de interação e desempenho (conforme os modelos `InteractionLog` e `PerformanceMetric` esboçados), treinar modelos específicos e criar endpoints na API (ou views no Django) para fornecer as previsões/recomendações aos dashboards.

## Próximos Passos no Desenvolvimento

*   Implementar as funcionalidades específicas listadas nos links "(Funcionalidade a implementar)" em cada dashboard.
*   Desenvolver os modelos de dados restantes (Classroom, Activity, Assignment, Submission, Logs, Metrics).
*   Criar formulários para adição/edição de dados (escolas, professores, alunos, atividades).
*   Implementar testes unitários e de integração mais robustos.
*   Refinar a interface do usuário (UI/UX).
*   Integrar as funcionalidades de Machine Learning planejadas.

