from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()



class TaskList(SelectRelatedMixin, generic.ListView):
    model = models.Task
    select_related = ("user",'message')


class TaskDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Task
    select_related = ("user")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateTask(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.taskForm
    fields = ('message')
    model = models.Task
