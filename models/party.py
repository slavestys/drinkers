import random
import logging
import json

from application import Application


from models.drinker import Drinker
from models.drink import Drink


class Party:
    STATE_NORMAL = 1
    STATE_GOOD_END = 2
    STATE_BAD_END = 3

    STATE_NAMES = {
        STATE_NORMAL: 'normal',
        STATE_GOOD_END: 'good_end',
        STATE_BAD_END: 'bad_end'
    }

    def __init__(self, drinkers=None, drinks=None):
        self.state = Party.STATE_NORMAL
        self.messages = []
        if drinkers is None:
            self.drinkers = []
        else:
            self.drinkers = drinkers

        for drinker in self.drinkers:
            drinker.party = self

        if drinks is None:
            self.drinks = []
        else:
            self.drinks = drinks
        self.changed = False

    def clean(self):
        self.state = Party.STATE_NORMAL
        self.messages = []
        self.drinkers = []
        self.drinks = []
        self.changed = True

    def add_drinker(self, drinker):
        logging.info('add drinker name {0} endurance {1}'.format(drinker.name, drinker.endurance))
        drinker.party = self
        self.drinkers.append(drinker)
        self.changed = True

    def add_drink(self, drink):
        logging.info('add drink name {0} degrees {1} quantity {2}'.format(drink.name, drink.degrees, drink.quantity))
        self.drinks.append(drink)
        self.changed = True

    def tick(self):
        any_drinks = 0
        if self.drinks:
            for drinker in self.drinkers:
                if not self.drinks:
                    return 0
                drink = random.choice(self.drinks)
                if drinker.drink(drink):
                    any_drinks = 1
                    if not drink.quantity:
                        self.drinks.remove(drink)
        return any_drinks

    def is_all_drunk(self):
        for drinker in self.drinkers:
            if drinker.state == Drinker.STATE_NORMAL:
                return 0
        return 1

    def party_hard(self):
        iteration_number = 1
        self.messages.append('Party start')
        logging.info('Party start')
        while self.state == Party.STATE_NORMAL:
            self.messages.append('Party hard {0}'.format(iteration_number))
            any_drinks = self.tick()
            if not any_drinks:
                if self.is_all_drunk():
                    self.state = Party.STATE_GOOD_END
                else:
                    self.state = Party.STATE_BAD_END
            iteration_number += 1
        msg = 'Party is over: {0}'.format(Party.STATE_NAMES[self.state])
        logging.info(msg)
        self.messages.append(msg)
        self.changed = True

    def to_save_data(self):
        drinkers_to_client = []
        for drinker in self.drinkers:
            drinkers_to_client.append(drinker.to_client())
        drinks_to_client = []
        for drink in self.drinks:
            drinks_to_client.append(drink.to_client())
        data = {
            'drinkers': drinkers_to_client,
            'drinks': drinks_to_client,
            'state': self.state
        }
        return data

    def to_client(self):
        data = self.to_save_data()
        party_messages = self.messages
        if party_messages:
            data['messages'] = party_messages

        return data

    def save(self):
        save_data = json.dumps(self.to_save_data())
        Application.redis.set('party', save_data)
        self.changed = False

    @classmethod
    def load(cls):
        data = Application.redis.get('party')
        drinkers = []
        drinks = []
        state = cls.STATE_NORMAL
        if data:
            parsed_data = json.loads(data.decode('utf-8'))
            for drinker_data in parsed_data['drinkers']:
                drinkers.append(Drinker.from_redis(drinker_data))
            for drink_data in parsed_data['drinks']:
                drinks.append(Drink.from_redis(drink_data))
            state = parsed_data['state']

        party = Party(drinkers, drinks)
        party.state = state
        return party










