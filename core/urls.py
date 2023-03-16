from django.urls import path
from . import views

urlpatterns = [
    path("objects/<int:pk>/", views.object, name="object"),
    path("objects/", views.list_objects, name="list objects"),
]
