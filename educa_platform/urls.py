# educa_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Para redirecionar a raiz

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")), # URLs padrão substituídas por allauth
    path("accounts/", include("allauth.urls")), # Inclui URLs do django-allauth (login, logout, signup, social, etc.)
    path("dashboards/", include("dashboards.urls")), # Inclui as URLs do app dashboards
    path("api/v1/", include("api.urls")), # Inclui as URLs da API

    # Redireciona a rota raiz para a página de login do allauth (CORRIGIDO)
    path("", RedirectView.as_view(pattern_name="account_login"), name="root_redirect"),
]

