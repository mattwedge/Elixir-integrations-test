from core.models import (
    BooleanForm,
    CharacterForm,
    DateForm,
    FloatForm,
    IntegerForm,
    TextForm,
    URLForm,
)
from core.types import FieldType


def get_form_model(form_type: FieldType):
    """Get the form model associated to a specific field type"""
    if form_type == "CHAR":
        return CharacterForm
    if form_type == "TEXT":
        return TextForm
    if form_type == "INTEGER":
        return IntegerForm
    if form_type == "FLOAT":
        return FloatForm
    if form_type == "BOOLEAN":
        return BooleanForm
    if form_type == "DATE":
        return DateForm
    if form_type == "URL":
        return URLForm

    raise TypeError(f"No form model found for type {form_type}")
