import random
from drinker import Drinker

class Party:
    STATE_NORMAL = 1
    STATE_GOOD_END = 2
    STATE_BAD_END = 3

    STATE_NAMES = {
        STATE_NORMAL: 'normal',
        STATE_GOOD_END: 'good_end',
        STATE_BAD_END: 'bad_end'
    }

    def __init__(self, drinkers = None, drinks = None):
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

    def add_drinker(self, drinker):
        drinker.party = self
        self.drinkers.append(drinker)

    def add_drink(self, drink):
        self.drinks.append(drink)

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
        while self.state == Party.STATE_NORMAL:
            self.messages.append('Party hard {0}'.format(iteration_number))
            any_drinks = self.tick()
            if not any_drinks:
                if self.is_all_drunk():
                    self.state = Party.STATE_GOOD_END
                else:
                    self.state = Party.STATE_BAD_END
            iteration_number += 1
        self.messages.append('Party is over: {0}'.format(Party.STATE_NAMES[self.state]))

    def messages_to_client(self):
        if not self.messages:
            return None
        to_client_messages = self.messages
        self.messages = []
        return to_client_messages











