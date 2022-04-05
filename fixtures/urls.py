from django.urls import path

from . import views

urlpatterns = [
    path("<int:matchday>", views.fixtures, name="fixtures"),

]