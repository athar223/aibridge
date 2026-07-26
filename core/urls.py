from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("recommender/", views.recommender, name="recommender"),
    path("prompt-generator/", views.prompt_generator, name="prompt_generator"),
    path("resources/", views.resources, name="resources"),
    path("contact/", views.contact, name="contact"),
]
