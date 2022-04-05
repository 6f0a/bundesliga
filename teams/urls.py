from django.urls import path

from . import views

urlpatterns = [
    path("", views.teams, name="teams"),
    path("<int:id>", views.team_detail, name="team_detail"),
]