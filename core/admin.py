from django.contrib import admin
from core.models import Service, Field, CharacterForm, IntegerForm, FloatForm, TextForm, Object

admin.site.register(Service)
admin.site.register(Object)
admin.site.register(Field)
admin.site.register(IntegerForm)
admin.site.register(FloatForm)
admin.site.register(CharacterForm)
admin.site.register(TextForm)
