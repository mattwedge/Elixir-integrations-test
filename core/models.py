from threading import Lock
from polymorphic.models import PolymorphicModel

from django.db import models, transaction


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Service: {str(self)}>"

class Object(models.Model):
    object_counter = models.IntegerField(default=0, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    counter_lock = Lock()

    def get_absolute_url(self):
        return f"/core/{self.service}/objects/{self.id}/"

    def save(self, force_insert=False, force_update=False, **kwargs):
        if not self.id:
            self.allocate_next_object_counter(force_insert, force_update, **kwargs)

        update = True
        current = None

        try:
            current = Object.objects.get(pk=self.id)

        except Object.DoesNotExist:
            current = None
            update = False

        super(Object, self).save(force_insert, force_update, **kwargs)

    def allocate_next_object_counter(self, force_insert, force_update, **kwargs):
        similar_objects = Object.objects.filter(service=self.service)
        similar_objects = similar_objects.select_for_update().order_by('-object_counter')

        with Object.counter_lock, transaction.atomic():
            max_counter = 0

            """
            @NOTE
            It's possible that no objects may be returned and an attribute error
            will be thrown when accessing the object_counter of a non-existing first() element
            of a query set, so just catch and pass the error, it's non fatal but does have
            to be handled.
            """
            try:
                max_counter = similar_objects.first().object_counter

            except AttributeError:
                pass

            self.object_counter = max_counter + 1
            super(Object, self).save(force_insert, force_update, **kwargs)

    def __str__(self):
        return f"{self.service}-{self.object_counter}"

    def __repr__(self):
        return f"<Object: {str(self)}>"

class Field(models.Model):
    FORM_TYPES = (
        ("CHAR", "SHORT TEXT (Titles, Names etc)"),
        ("TEXT", "LARGE TEXT (Rich Text Editor)"),
        ("INTEGER", "INTEGER"),
        ("FLOAT", "DECIMAL (i.e., Amount (g) = 23.72)"),
        ("BOOLEAN", "CHECKBOX (True / False)"),
    )

    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    form_type = models.CharField(max_length=8, choices=FORM_TYPES)
    order = models.IntegerField(default=1)

    def save(self, **kwargs):
        if not self.id and (max_counter := Field.objects.filter(object=self.object).order_by('-order')):
            self.order = max_counter[0].order + 1  if max_counter else 1

        super(Field, self).save(**kwargs)

    def __str__(self):
        return f"{self.object}: {self.name} ({self.form_type})"

    def __repr__(self):
        return f"<Field: {str(self)}>"

class Form(PolymorphicModel):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = None

    def __str__(self):
        return f"{self.field.name} - {self.value}"

class IntegerForm(Form):
    type = models.CharField(default='int', editable=False, max_length=3)
    value = models.IntegerField(default=0, null=True, blank=True)

class FloatForm(Form):
    type = models.CharField(default='float', editable=False, max_length=5)
    value = models.FloatField(default=0.0, null=True, blank=True)

class CharacterForm(Form):
    type = models.CharField(default='char', editable=False, max_length=4)
    value = models.CharField(max_length=255, default="", null=True, blank=True)

class TextForm(Form):
    type = models.CharField(default='text', editable=False, max_length=4)
    value = models.TextField(default="", null=True, blank=True)

class BooleanForm(Form):
    type = models.CharField(default='bool', editable=False, max_length=4)
    value = models.BooleanField(default=False, null=True, blank=True)
