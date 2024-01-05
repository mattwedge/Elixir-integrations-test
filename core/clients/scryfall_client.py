import json
import os
import requests
from core.clients.base_client import BaseClient

SCRYFALL_BASE_URL = "https://api.scryfall.com"


class ScryfallClient(BaseClient):
    """A client to integrate with the MTG api - https://api.scryfall.com"""

    service_name = "Magic The Gathering Cards"
    service_description = "A repository of existing MTG cards"
    json_fields = {
        "source_id": {
            "type": "CHAR",
            "description": "The ID of the card in the source API",
            "order": 1,
        },
        "oracle_id": {
            "type": "CHAR",
            "description": "The Oracle ID of the card",
            "order": 2,
        },
        "mtgo_id": {
            "type": "INTEGER",
            "description": "The MTGO ID of the card",
            "order": 3,
        },
        "cardmarket_id": {
            "type": "INTEGER",
            "description": "The CardMarket ID of the card",
            "order": 4,
        },
        "name": {
            "type": "CHAR",
            "description": "The name of the card",
            "order": 5,
        },
        "lang": {
            "type": "CHAR",
            "description": "The language of the card",
            "order": 6,
        },
        "released_at": {
            "type": "DATE",
            "description": "The date of release of the card",
            "order": 7,
        },
        "highres_image": {
            "type": "BOOLEAN",
            "description": "Whether the card has a high-resolution image",
            "order": 8,
        },
    }

    def __init__(self, json_save_location="/tmp/"):
        super().__init__()
        self.printed_num_lines = False
        self.json_save_location = json_save_location

        if not os.path.exists(json_save_location):
            os.makedirs(json_save_location)

    def retrieve_object_json(self, batch_number):
        res = requests.get(f"{SCRYFALL_BASE_URL}/bulk-data")
        res_json = res.json()
        json_download_uri = [
            obj for obj in res_json["data"] if obj["type"] == "all_cards"
        ][0]["download_uri"]

        file_name = json_download_uri.split("/")[-1]
        file_location = f"{self.json_save_location}{file_name}"

        if not os.path.exists(file_location):
            self.logger.info(f"No JSON file found at {file_location} - downloading")
            res = requests.get(json_download_uri)

            with open(file_location, "wb") as file:
                file.write(res.content)

        num_items_per_batch = 3000
        batch_rows = []

        start_line = ((batch_number - 1) * num_items_per_batch) + 1
        end_line = (batch_number * num_items_per_batch) + 1

        if not self.printed_num_lines:
            with open(file_location, "r") as file:
                num_lines = sum(1 for line in file)
                self.logger.info(f"File has {num_lines} rows to process")
                self.printed_num_lines = True

        with open(file_location, "r") as file:
            self.logger.info(f"Extracting rows {start_line} to {end_line}")
            for line_number, line in enumerate(file):
                if line_number == end_line:
                    break
                if line.strip() == "]":
                    # This is the last line
                    break
                if line_number >= start_line:
                    batch_rows.append(json.loads(line.strip()[:-1]))

        values = [{**datum, "source_id": datum["id"]} for datum in batch_rows]

        return values
