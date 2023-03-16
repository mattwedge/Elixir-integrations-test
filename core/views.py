from django.shortcuts import render, get_object_or_404

from . import models

def object(request, pk: int):
    object = get_object_or_404(models.Object, pk=pk)
    data = {
        field.name: models.Form.objects.filter(object=object, field=field).first()
        for field in models.Field.objects.filter(object=object)
    }

    return render(request, "core/object.html", {"object": object, "data": data})

def list_objects(request):
    return render(request, "core/objects.html", {"objects": models.Object.objects.all()})
