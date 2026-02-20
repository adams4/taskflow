from time import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskForm 


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion auto après inscription
            messages.success(request, "Compte créé avec succès ! Bienvenue sur TaskFlow.")
            return redirect('task_list')
        else:
            messages.error(request, "Erreur lors de la création du compte. Vérifiez les champs.")
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = "Tâche créée avec succès !"

    def form_valid(self, form):
        form.instance.user = self.request.user  # lie la tâche à l'utilisateur connecté
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = "Tâche modifiée avec succès !"

    def get_queryset(self):
        # Sécurité : seul le propriétaire peut modifier
        return Task.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    success_message = "Tâche supprimée."
    template_name = 'tasks/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    tasks = self.get_queryset()
    context['total_tasks'] = tasks.count()
    context['todo_tasks'] = tasks.filter(status='TODO').count()
    context['overdue_tasks'] = tasks.filter(due_date__lt=timezone.now(), status__in=['TODO', 'IN_PROGRESS']).count()
    return context