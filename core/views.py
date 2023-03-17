from django.views.generic import ListView
from django.core.serializers import serialize
from django.http import JsonResponse

from . import models


class ServiceView(ListView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "services": [{"name": s.name, "description": s.description} for s in models.Service.objects.all()]
        })
