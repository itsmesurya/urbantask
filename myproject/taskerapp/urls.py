from django.conf.urls import url

from . import views

app_name='taskerapp'

urlpatterns = [
    url(r"^$", views.TaskList.as_view(), name="all"),
]
