# core/models.py

from django.db import models
from django.conf import settings
from accounts.models import TeacherProfile, StudentProfile, User # Importar User também

class Subject(models.Model):
    """Modelo para representar disciplinas."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    """Modelo para representar atividades criadas pelos professores."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="activities")
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Campo para anexos (pode ser melhorado com um modelo separado ou usando bibliotecas como django-filer)
    attachment = models.FileField(upload_to="activity_attachments/", blank=True, null=True)

    def __str__(self):
        # Corrigido: f-string e aspas
        teacher_name = self.teacher.user.get_full_name() if self.teacher and self.teacher.user else "Professor Desconhecido"
        return f"{self.title} por {teacher_name}"

class Submission(models.Model):
    """Modelo para representar a submissão de uma atividade por um aluno."""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True) # Resposta textual
    attachment = models.FileField(upload_to="submission_attachments/", blank=True, null=True) # Anexo do aluno
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # Nota dada pelo professor
    feedback = models.TextField(blank=True, null=True) # Feedback do professor
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Corrigido: aspas duplas internas
        unique_together = (("activity", "student"),) # Um aluno só pode submeter uma vez por atividade

    def __str__(self):
        # Corrigido: f-string e aspas
        student_name = self.student.user.get_full_name() if self.student and self.student.user else "Aluno Desconhecido"
        activity_title = self.activity.title if self.activity else "Atividade Desconhecida"
        return f"Submissão para '{activity_title}' por {student_name}"

class InteractionLog(models.Model):
    """Modelo para registrar interações do aluno com a plataforma (visualização, tempo gasto, etc.)."""
    ACTION_CHOICES = [
        # Corrigido: aspas duplas internas
        ("VIEW_ACTIVITY", "Visualizou Atividade"),
        ("START_ACTIVITY", "Iniciou Atividade"),
        ("SUBMIT_ACTIVITY", "Submeteu Atividade"),
        ("VIEW_FEEDBACK", "Visualizou Feedback"),
        # Adicionar outras ações relevantes
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="interactions")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True, related_name="interactions")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True) # Para dados extras, como tempo gasto

    def __str__(self):
        # Corrigido: f-string
        student_name = self.student.user.get_full_name() if self.student and self.student.user else "Aluno Desconhecido"
        return f"{student_name} - {self.get_action_display()} em {self.timestamp}"

class PerformanceMetric(models.Model):
    """Modelo para armazenar métricas de desempenho calculadas (ex: engajamento, atenção)."""
    METRIC_CHOICES = [
        # Corrigido: aspas duplas internas
        ("ENGAGEMENT_SCORE", "Pontuação de Engajamento"),
        ("ATTENTION_LEVEL", "Nível de Atenção Estimado"),
        ("COMPLETION_RATE", "Taxa de Conclusão"),
        # Adicionar outras métricas
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="metrics")
    metric_type = models.CharField(max_length=50, choices=METRIC_CHOICES)
    value = models.FloatField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    related_activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name="metrics")
    related_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="metrics")

    class Meta:
        # Corrigido: aspas duplas internas
        ordering = ["-calculated_at"]

    def __str__(self):
        # Corrigido: f-string
        student_name = self.student.user.get_full_name() if self.student and self.student.user else "Aluno Desconhecido"
        return f"{student_name} - {self.get_metric_type_display()}: {self.value}"

