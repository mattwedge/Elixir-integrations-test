from django.test import TestCase

from core.clients.base_client import BaseClient
from core.models import Field, Form, Object, Service
from core.utils.get_form_model import get_form_model


test_service_name = "__SERVICE_NAME__"
test_service_description = "__SERVICE_DESCRIPTION__"
test_json_fields = {
    "char": {
        "type": "CHAR",
        "description": "__CHAR_FIELD_DESCRIPTION__",
        "order": 1,
    }
}
test_object_json = [{"char": "__CHAR_VALUE__"}]


class ValidTestClient(BaseClient):
    """A valid test client that mocks the external calls in a real client"""

    service_name = test_service_name
    service_description = test_service_description
    json_fields = test_json_fields

    def retrieve_object_json(self):
        return test_object_json


class NoFieldTestClient(BaseClient):
    """An invalid test client that does not set json_fields"""

    service_name = test_service_name
    service_description = test_service_description

    def retrieve_object_json(self):
        return test_object_json


class NoServiceNameTestClient(BaseClient):
    """An invalid test client that does not include a service name"""

    service_description = test_service_description
    json_fields = test_json_fields

    def retrieve_object_json(self):
        return test_object_json


class NoServiceDescriptionTestClient(BaseClient):
    """An invalid test client that does not include a service description"""

    service_name = test_service_name
    json_fields = test_json_fields

    def retrieve_object_json(self):
        return test_object_json


class NoRetrieveTestClient(BaseClient):
    """An invalid test client that does not override the retrieve_object_json method"""

    service_description = test_service_description
    service_name = test_service_name
    json_fields = test_json_fields


class BaseClientTests(TestCase):
    """Tests for the abstract base client for integrations"""

    def test_cannot_instantiate_without_json_fields(self):
        """Test that a BaseClient subclass requires json_fields"""
        with self.assertRaises(TypeError):
            client = NoFieldTestClient()

    def test_cannot_instantiate_without_service_name(self):
        """Test that a BaseClient subclass requires service_name"""
        with self.assertRaises(TypeError):
            client = NoServiceNameTestClient()

    def test_cannot_instantiate_without_service_description(self):
        """Test that a BaseClient subclass requires service_description"""
        with self.assertRaises(TypeError):
            client = NoServiceDescriptionTestClient()

    def test_cannot_instantiate_without_retrieve_object_json(self):
        """Test that a BaseClient subclass requires retrieve_object_json"""
        with self.assertRaises(TypeError):
            client = NoRetrieveTestClient()

    def test_valid_subclass(self):
        """Test that a valid subclass of BaseClient can be instantiated and
        the integration can be run"""

        initial_services = Service.objects.filter(name=test_service_name)
        self.assertEqual(initial_services.count(), 0)

        client = ValidTestClient()
        client.run_integration()

        final_services = Service.objects.filter(name=test_service_name)
        self.assertEqual(final_services.count(), 1)

        service = final_services.first()

        final_objects = Object.objects.filter(service=service)
        self.assertEqual(final_objects.count(), len(test_json_fields))

        for test_object in test_object_json:
            for name, value in test_object.items():
                FormModel = get_form_model(test_json_fields[name]["type"])
                field = Field.objects.get(service=service, name=name)
                forms = FormModel.objects.filter(field=field, value=value)

                # There should be one form per field for each object
                self.assertEqual(forms.count(), len(test_json_fields))
