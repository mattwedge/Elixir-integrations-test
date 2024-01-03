from abc import ABC, abstractmethod
from typing import Any, List, TypedDict, Dict

from core.models import (
    BooleanForm,
    CharacterForm,
    DateForm,
    Field,
    FloatForm,
    IntegerForm,
    Object,
    Service,
    TextForm,
    URLForm,
)
from core.types import FieldType
from core.utils.get_form_model import get_form_model
from core.utils.logger import Logger


class IntegrationError(Exception):
    """Raise a custom error for integrations"""


class FieldAttributes(TypedDict):
    """The type of the field attributes to be defined in json_fields"""

    type: FieldType
    description: str
    order: int


class BaseClient(ABC):
    def __init__(self):
        self.service = None
        self.json_objects = []
        self.logger = Logger(self.service_name)

    @property
    @abstractmethod
    def json_fields(self) -> Dict[str, FieldAttributes]:
        """Defines the fields to be parsed from the JSON objects that are
        retrieved from the API"""

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Defines the name of the service"""

    @property
    @abstractmethod
    def service_description(self) -> str:
        """A description of the service"""

    @abstractmethod
    def retrieve_object_json(self, batch_number: int) -> List[Any]:
        """Get a list of JSON objects from the given API.

        Should return [] if the batch is empty and this will trigger the end
        of the process. i.e. no more batches will be processed
        """

    def _set_object_json(self, batch_number):
        """Retrieve JSON objects from the given API and set them on the client instance"""
        self.json_objects = self.retrieve_object_json(batch_number)

    def _clear_data(self):
        """Clear any existing data

        NOTE: In theory this should just work with `services.delete()` but we actually
        get a ForeignKey constraint error, possibly something to do with django-polymorphic
        """
        # We can rely on models.CASCADE to delete all associated objects and fields etc
        self.logger.info(f"Deleting service {self.service_name}")
        services = Service.objects.filter(name=self.service_name)
        objects = Object.objects.filter(service__in=services)
        fields = Field.objects.filter(service__in=services)

        form_types = [
            IntegerForm,
            FloatForm,
            CharacterForm,
            TextForm,
            BooleanForm,
            DateForm,
            URLForm,
        ]
        for FormModel in form_types:
            forms = FormModel.objects.filter(field__in=fields)
            forms.delete()

        fields.delete()
        objects.delete()
        services.delete()

    def _setup_models(self):
        """Set up the service and fields for this service"""
        self.logger.info(f"Creating Service {self.service_name}")
        self.service = Service.objects.create(
            name=self.service_name, description=self.service_description
        )
        for field, attrs in self.json_fields.items():
            self.logger.info(f"Creating Field {field}")
            Field.objects.create(
                service=self.service,
                name=field,
                form_type=attrs["type"],
                description=attrs["description"],
                order=attrs["order"],
            )

    def _save_objects(self):
        """Save the objects in self.json_objects"""
        self.logger.info(f"Saving {len(self.json_objects)} objects")
        for json_object in self.json_objects:
            new_object = Object.objects.create(service=self.service)

            for name, value in json_object.items():
                if name not in self.json_fields:
                    continue

                field = Field.objects.get(service=self.service, name=name)

                Form = get_form_model(self.json_fields[name]["type"])
                Form.objects.create(
                    object=new_object,
                    field=field,
                    value=value,
                )

    def run_integration(self):
        """The entrypoint to run the integration"""
        self._clear_data()
        self._setup_models()

        batch_number = 1
        while True:
            self._set_object_json(batch_number)
            if not self.json_objects:
                break

            self._save_objects()
            batch_number += 1
