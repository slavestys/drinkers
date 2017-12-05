import json

from party import Party
from drinker import Drinker
from drink import Drink


class PartyController:
    party = Party()
    errors = []

    @staticmethod
    def prepare_parameter(parameters, name, cast_method = None):
        list_value = parameters.get(name)
        value = list_value[0].decode('utf-8') if list_value and len(list_value) > 0 else None
        if not value:
            raise ValueError("parameter {0} should be present".format(name.decode('utf-8')))

        if cast_method:
            try:
                value = cast_method(value)
            except Exception:
                raise TypeError("parameter {0} has wrong type".format(name.decode('utf-8')))
        return value

    @staticmethod
    def invoke(method, params):
        if method:
            try:
                getattr(PartyController, method)(params)
            except Exception as ex:
                PartyController.errors.append(str(ex))
        return PartyController.to_client()

    @staticmethod
    def add_drinker(parameters):
        name = PartyController.prepare_parameter(parameters, b'name')
        endurance = PartyController.prepare_parameter(parameters, b'endurance', int)
        drinker = Drinker(name, endurance)
        PartyController.party.add_drinker(drinker)

    @staticmethod
    def add_drink(parameters):
        name = PartyController.prepare_parameter(parameters, b'name')
        degrees = PartyController.prepare_parameter(parameters, b'degrees', int)
        quantity = PartyController.prepare_parameter(parameters, b'quantity', int)
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

