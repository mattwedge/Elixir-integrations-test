from unittest.mock import MagicMock, patch

from django.test import TestCase

from core.clients.pokemon_client import PokemonClient
from core.models import CharacterForm, Field, Object, Service

DEFAULT_POKEMON = {
    "id": "__DEFAULT_ID__",
    "name": "__DEFAULT_NAME__",
    "supertype": "__DEFAULT_SUPERTYPE__",
    "level": "1",
    "hp": "1",
    "evolvesFrom": "__DEFAULT_EVOLVES_FROM__",
    "number": "1",
    "artist": "__DEFAULT_ARTIST__",
    "rarity": "__DEFAULT_RARITY__",
    "flavorText": "__DEFAULT_FLAVOUR_TEXT__",
}


class MockResponse:
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def raise_for_status(self):
        return True

    def json(self):
        return self.data


class PokemonClientTests(TestCase):
    """Tests for the Pokemon client for integrations"""

    @patch("core.clients.pokemon_client.requests")
    def test_client_single_page(self, mrequests):
        """Test that the client works as expected"""
        self.assertFalse(Service.objects.filter(name="Pokemon Cards").exists())

        mrequests.get = MagicMock()

        # The first request should give 2 pokemon cards
        # and the second request should give none
        mrequests.get.side_effect = [
            MockResponse(
                data={
                    "pageSize": 250,
                    "count": 2,
                    "page": 1,
                    "data": [
                        {**DEFAULT_POKEMON},
                        {
                            **DEFAULT_POKEMON,
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

        client = PokemonClient()
        client.run_integration()

        self.assertTrue(Service.objects.filter(name="Pokemon Cards").exists())

        service = Service.objects.filter(name="Pokemon Cards").first()
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
