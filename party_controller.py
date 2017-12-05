import json

from party import Party
from drinker import Drinker
from drink import Drink


class PartyController:
    party = Party()
    errors = []

    @staticmethod
    def invoke(method, params):
        if method:
            try:
                getattr(PartyController, method)(params)
            except Exception as ex:
                PartyController.errors.append(ex)
        return PartyController.to_client()

    @staticmethod
    def add_drinker(parameters):
        name = parameters[b'name'][0].decode('utf-8')
        endurance = int(parameters[b'endurance'][0].decode('utf-8'))
        drinker = Drinker(name, endurance)
        PartyController.party.add_drinker(drinker)

    @staticmethod
    def add_drink(parameters):
        name = parameters[b'name'][0].decode('utf-8')
        degrees = int(parameters[b'degrees'][0].decode('utf-8'))
        quantity = int(parameters[b'quantity'][0].decode('utf-8'))
        drink = Drink(name, degrees, quantity)
        PartyController.party.add_drink(drink)

    @staticmethod
    def party_hard(parameters):
        PartyController.party.party_hard()

    @staticmethod
    def to_client():
        drinkers_to_client = []
        for drinker in PartyController.party.drinkers:
            drinkers_to_client.append(drinker.to_client())
        drinks_to_client = []
        for drink in PartyController.party.drinks:
            drinks_to_client.append(drink.to_client())
        data = {
            'drinkers': drinkers_to_client,
            'drinks': drinks_to_client,
            'state': PartyController.party.state
        }
        party_messages = PartyController.party.messages
        if party_messages:
            data['messages'] = party_messages
        if PartyController.errors:
            data['errors'] = PartyController.errors
            PartyController.errors = []
        return json.dumps(data)

