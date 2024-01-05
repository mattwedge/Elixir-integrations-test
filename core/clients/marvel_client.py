import hashlib
import os
import time
import requests
from core.clients.base_client import BaseClient

MARVEL_BASE_URL = "http://gateway.marvel.com/v1/public"


class MarvelClient(BaseClient):
    """A client to integrate with the Marvel api - https://gateway.marvel.com"""

    service_name = "Marvel Characters"
    service_description = "A repository of Marvel characters"
    json_fields = {
        "source_id": {
            "type": "CHAR",
            "description": "The ID of the character in the source API",
            "order": 1,
        },
        "name": {
            "type": "CHAR",
            "description": "The name of the character",
            "order": 2,
        },
        "description": {
            "type": "TEXT",
            "description": "A description of the character",
            "order": 3,
        },
    }

    def retrieve_object_json(self, batch_number):
        num_pages_per_batch = 10
        num_results_per_page = 100
        public_api_key = os.getenv("MARVEL_PUBLIC_KEY")
        private_api_key = os.getenv("MARVEL_PRIVATE_KEY")
        ts = int(time.time())
        hash = hashlib.md5(
            f"{ts}{private_api_key}{public_api_key}".encode("utf-8")
        ).hexdigest()

        values = []

        next_page_number = (batch_number - 1) * num_pages_per_batch
        while True:
            next_page_number += 1
            offset = num_results_per_page * (next_page_number - 1)
            self.logger.info(f"Requesting page {next_page_number}")
            res = requests.get(
                f"{MARVEL_BASE_URL}/characters?limit={num_results_per_page}&apikey={public_api_key}&ts={ts}&hash={hash}&offset={offset}",
                proxies={"http": None, "https": None},
            )
            res_json = res.json()

            parsed_json = [
                {**datum, "source_id": datum["id"]}
                for datum in res_json["data"]["results"]
            ]

            values += parsed_json

            if res_json["data"]["count"] < num_results_per_page:
                break

            if next_page_number >= batch_number * num_pages_per_batch:
                break

        return values
