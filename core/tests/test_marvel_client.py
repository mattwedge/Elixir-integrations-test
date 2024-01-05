from unittest.mock import MagicMock, patch

from django.test import TestCase
from core.clients.marvel_client import MarvelClient

from core.models import CharacterForm, Field, Object, Service

DEFAULT_CHARACTER = {
    "id": "__DEFAULT_ID__",
    "name": "__DEFAULT_NAME__",
    "description": "__DEFAULT_DESCRIPTION__",
}


class MockResponse:
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def raise_for_status(self):
        return True

    def json(self):
        return self.data


class MarvelClientTests(TestCase):
    """Tests for the Marvel client for integrations"""

    @patch("core.clients.marvel_client.requests")
    def test_client_single_page(self, mrequests):
        """Test that the client works as expected"""
        self.assertFalse(Service.objects.filter(name="Marvel Characters").exists())

        mrequests.get = MagicMock()

        # The first request should give 2 Marvel characters
        # and the second request should give none
        mrequests.get.side_effect = [
            MockResponse(
                data={
                    "pageSize": 250,
                    "count": 2,
                    "page": 1,
                    "data": [
                        {**DEFAULT_CHARACTER},
                        {
                            **DEFAULT_CHARACTER,
                            "id": "__OTHER_ID__",
                            "name": "__OTHER_NAME__",
                        },
                    ],
                }
            ),
            MockResponse(
                data={
                    "pageSize": 250,
                    "count": 0,
                    "page": 2,
                    "data": [],
                }
            ),
        ]

        client = MarvelClient()
        client.run_integration()

        self.assertTrue(Service.objects.filter(name="Marvel Characters").exists())

        service = Service.objects.filter(name="Marvel Characters").first()
        self.assertEqual(Object.objects.filter(service=service).count(), 2)

        first_object = Object.objects.first()

        name_field = Field.objects.get(name="name", service=service)

        self.assertTrue(
            CharacterForm.objects.filter(
                object=first_object, field=name_field, value="__DEFAULT_NAME__"
            ).exists()
        )

        last_object = Object.objects.last()
        self.assertTrue(
            CharacterForm.objects.filter(
                object=last_object, field=name_field, value="__OTHER_NAME__"
            ).exists()
        )
