from core.clients.marvel_client import MarvelClient
from core.clients.pokemon_client import PokemonClient
from core.clients.scryfall_client import ScryfallClient


def main():
    pokemon_client = PokemonClient()
    pokemon_client.run_integration()

    scryfall_client = ScryfallClient()
    scryfall_client.run_integration()

    marvel_client = MarvelClient()
    marvel_client.run_integration()
