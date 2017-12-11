import json
import logging

from models.party import Party
from models.drinker import Drinker
from models.drink import Drink


class PartyController:

    def __init__(self):
        self.errors = []
        self.party = Party.load()
        if not self.party:
            self.party = Party()

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

    def invoke(self, method, params):
        if method:
            try:
                getattr(self, method)(params)
                if self.party.changed:
                    self.party.save()
            except Exception as ex:
                msg = str(ex)
                logging.error(msg)
                self.errors.append(msg)
        return self.to_client()

    def add_drinker(self, parameters):
        name = PartyController.prepare_parameter(parameters, b'name')
        endurance = PartyController.prepare_parameter(parameters, b'endurance', int)
        drinker = Drinker(name, endurance)
        self.party.add_drinker(drinker)

    def add_drink(self, parameters):
        name = PartyController.prepare_parameter(parameters, b'name')
        degrees = PartyController.prepare_parameter(parameters, b'degrees', int)
        quantity = PartyController.prepare_parameter(parameters, b'quantity', int)
        drink = Drink(name, degrees, quantity)
        self.party.add_drink(drink)

    def party_hard(self, parameters):
        self.party.party_hard()

    def party_clean(self, parameters):
        self.party.clean()

    def to_client(self):
        data = self.party.to_client()
        if self.errors:
            data['errors'] = self.errors
            self.errors = []
        return json.dumps(data)

