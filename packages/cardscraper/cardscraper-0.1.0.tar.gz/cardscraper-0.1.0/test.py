from cardscraper import generate_anki_package, get_plugin_by_group_and_name
from cardscraper.__main__ import read_yaml_file
from cardscraper.generate import Config, Module
from genanki import Model, Note

if __name__ == '__main__':
    config = read_yaml_file('/path/to/config.yaml')
    # or
    # config: Config = {...}

    get_model = get_plugin_by_group_and_name(Module.MODEL, 'default')
    get_deck = get_plugin_by_group_and_name(Module.DECK, 'default')
    get_package = get_plugin_by_group_and_name(Module.PACKAGE, 'default')

    def get_notes(config: Config, model: Model) -> list[Note]:
        notes = []
        ...
        return notes

    generate_anki_package(config, get_model, get_notes, get_deck, get_package)
