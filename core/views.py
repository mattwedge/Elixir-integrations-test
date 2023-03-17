from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView
from django.http import JsonResponse

from . import models

def object(request, service: str, pk: int):
    object = get_object_or_404(models.Object, pk=pk)
    data = {
        field.name: models.Form.objects.filter(object=object, field=field).first()
        for field in models.Field.objects.filter(object=object)
    }

    return render(request, "core/object.html", {"object": object, "data": data})

class AllObjects(ListView):
    model = models.Object
