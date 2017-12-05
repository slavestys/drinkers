import json

from party import Party
from drinker import Drinker
from drink import Drink


class PartyController:
    party = Party()

    @staticmethod
    def invoke(method, params):
        if method:
            getattr(PartyController, method)(params)
        return PartyController.to_client()

    @staticmethod
    def add_drinker(parameters):
        drinker = Drinker(parameters[b'name'][0].decode('utf-8'), int(parameters[b'endurance'][0].decode('utf-8')))
        PartyController.party.add_drinker(drinker)

    @staticmethod
    def add_drink(parameters):
        drink = Drink(parameters[b'name'][0].decode('utf-8'), int(parameters[b'degrees'][0].decode('utf-8')), int(parameters[b'quantity'][0].decode('utf-8')))
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
        return json.dumps(data)

