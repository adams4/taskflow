from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Basse'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Haute'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('DONE', 'Terminé'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name="Priorité"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TODO',
        verbose_name="Statut"
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date limite"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifiée le")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Utilisateur"
    )

    class Meta:
        ordering = ['-created_at']  # Les plus récentes en premier
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def is_overdue(self):
        if self.due_date and self.due_date < timezone.now():
            return True
        return False