from django.conf import settings
from django.urls import reverse
from django.db import models
from datetime import datetime    

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

TASK_CHOICES = (
    ('high','HIGH'),
    ('medium','MEDIUM'),
    ('low','LOW'),
)

class Task(models.Model):
    user_id = models.ForeignKey(User, related_name="taskerapp", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    dead_line = models.DateTimeField()
    message = models.CharField(max_length=20)
    priority = models.CharField(max_length=6, choices=TASK_CHOICES, default='medium')


    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

class TaskerState(object):

   name = "state"
   allowed = []

   def switch(self, state):
   	if state.name in self.allowed:
   		print ('Current:',self,' => switched to new state',state.name)
   		self.__class__ = state
   	else:
   		print ('Current:',self,' => switching to',state.name,'not possible.')

   def __str__(self):
    return self.name

class Off(TaskerState):
   name = "off"
   allowed = ['on']

class On(TaskerState):
   name = "on"
   allowed = ['off','suspend','hibernate']

class Suspend(TaskerState):
   name = "suspend"
   allowed = ['on']

class Hibernate(TaskerState):
   name = "hibernate"
   allowed = ['on']

class Tasker(object):
	def __init__(self, model='new'):
		self.model = model
		self.state = Off()

	def change(self, state):
		self.state.switch(state)

if __name__ == "__main__":
	comp = Tasker()
	comp.change(On)
	comp.change(Off)
	comp.change(On)
	comp.change(Suspend)
	comp.change(Hibernate)
	comp.change(On)
	comp.change(Off)

class Meta:
    ordering = ["-created_at"]
    unique_together = ['user','message']
