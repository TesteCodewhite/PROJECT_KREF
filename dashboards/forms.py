# dashboards/forms.py

from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Selecione o arquivo Excel (.xlsx)",
        help_text="O arquivo deve seguir o modelo fornecido e conter as colunas: aluno, série, turma, data_nacimento (DD/MM/AAAA), cpf (apenas números), email_escolar.",
        widget=forms.ClearableFileInput(attrs={"accept": ".xlsx"})
    )

