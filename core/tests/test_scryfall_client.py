import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from core.clients.scryfall_client import ScryfallClient

from core.models import CharacterForm, Field, Object, Service

DEFAULT_CARD = {
    "id": "__DEFAULT_ID__",
    "oracle_id": "__DEFAULT_ORACLE_ID__",
    "mtgo_id": 1,
    "cardmarket_id": 1,
    "name": "__DEFAULT_NAME__",
    "lang": "__DEFAULT_LANG",
    "released_at": "2000-10-10",
    "highres_image": True,
}


class MockResponse:
    def __init__(self, data, content=None, status_code=200):
        self.data = data
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        return True

    def json(self):
        return self.data


class ScryfallClientTests(TestCase):
    """Tests for the Scryfall client for integrations
    TODO: mock os and file access stuff
    """

    @patch("core.clients.scryfall_client.requests")
    def test_client(self, mrequests):
        """Test that the client works as expected"""
        self.assertFalse(
            Service.objects.filter(name="Magic The Gathering Cards").exists()
        )

        mrequests.get = MagicMock()

        # The first request should give the URI of the JSON file
        # and the second request should give none
        mrequests.get.side_effect = (
            [
                MockResponse(
                    data={
                        "data": [
                            {
                                "type": "all_cards",
                                "download_uri": "https://data.scryfall.io/all-cards/all-cards-20240103101329.json",
                            }
                        ]
                    }
                ),
                MockResponse(
                    data={},
                    content=f"""[
                    {json.dumps({**DEFAULT_CARD})},
                    {json.dumps({**DEFAULT_CARD, "name": "__OTHER_NAME__"})},
                ]""".encode(
                        "utf-8"
                    ),
                ),
            ]
            * 2
        )

        client = ScryfallClient()
        client.run_integration()

        self.assertTrue(
            Service.objects.filter(name="Magic The Gathering Cards").exists()
        )

        service = Service.objects.filter(name="Magic The Gathering Cards").first()
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
