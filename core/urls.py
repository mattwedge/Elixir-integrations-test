from django.urls import path
from . import views

urlpatterns = [
    path("<str:service>/objects/<int:pk>/", views.object, name="object"),
    path("<str:service>/objects/", views.AllObjects.as_view(), name="objects"),
]
