from django import forms

from taskerapp import models


class TaskForm(forms.ModelForm):
    class Meta:
        fields = ('message','created_at')
        model = models.Task