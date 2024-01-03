import requests
from core.clients.base_client import BaseClient

POKEMON_BASE_URL = "https://api.pokemontcg.io/v2"


class PokemonClient(BaseClient):
    """A client to integrate with the pokemon api - https://api.pokemontcg.io"""

    service_name = "Pokemon Cards"
    service_description = "A repository of existing pokemon cards"
    json_fields = {
        "source_id": {
            "type": "CHAR",
            "description": "The ID of the card in the source API",
            "order": 1,
        },
        "name": {"type": "CHAR", "description": "The name of the Pokemon", "order": 2},
        "supertype": {
            "type": "CHAR",
            "description": "The supertype of the Pokemon",
            "order": 3,
        },
        # Weirdly this is sometimes a string rather than an integer e.g. Torterra LV.X has Level "X"
        "level": {
            "type": "CHAR",
            "description": "The level of the Pokemon",
            "order": 4,
        },
        "hp": {
            "type": "INTEGER",
            "description": "The hitpoints of the Pokemon",
            "order": 5,
        },
        "evolvesFrom": {
            "type": "CHAR",
            "description": "The Pokemon that this is evolved from",
            "order": 6,
        },
        # Weirdly this is sometimes a string rather than an integer
        "number": {
            "type": "CHAR",
            "description": "The number of the Pokemon",
            "order": 7,
        },
        "artist": {
            "type": "CHAR",
            "description": "The artist who designed this Pokemon",
            "order": 8,
        },
        "rarity": {
            "type": "CHAR",
            "description": "The rarity of the Pokemon card",
            "order": 9,
        },
        "flavorText": {
            "type": "CHAR",
            "description": "A description of the Pokemon",
            "order": 10,
        },
    }

    def retrieve_object_json(self):
        values = []

        next_page_number = 0
        while True:
            next_page_number += 1
            self.logger.info(f"Requesting page {next_page_number}")
            res = requests.get(f"{POKEMON_BASE_URL}/cards?page={next_page_number}")
            res_json = res.json()
            parsed_json = [
                {**datum, "source_id": datum["id"]} for datum in res_json["data"]
            ]

            values += parsed_json

            if res_json["count"] < 250:
                break

            if res_json["page"] == 10:
                break

        return values
