from django.urls import path

from . import views

app_name= "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("wiki/<str:entry>", views.entry, name="entry")
]
