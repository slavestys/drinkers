import random
import logging

class Drinker:
    STATE_NORMAL = 1
    STATE_FUNNY = 2
    STATE_OUT = 3

    STATE_NAMES = {
        STATE_NORMAL: 'normal',
        STATE_FUNNY: 'funny',
        STATE_OUT: 'out'
    }

    STATE_FUNNY_PERCENT = (0.3, 0.6)
    STATE_OUT_PERCENT = (0, 0.4)

    def __init__(self, name, endurance):
        self.name = name
        self.endurance = endurance
        self.current_endurance = endurance
        self.state = Drinker.STATE_NORMAL

    @classmethod
    def from_redis(cls, data):
        drinker = Drinker(data['name'], data['endurance'])
        drinker.current_endurance = data['current_endurance']
        drinker.state = data['state']
        return drinker


    def drink(self, drink_object):
        if not (self.state == Drinker.STATE_NORMAL):
            return 0
        minimum = int(self.endurance / 4)
        maximum = int(self.endurance / 2)
        endurance_quantity = random.randint(minimum, maximum)
        if self.current_endurance < endurance_quantity:
            endurance_quantity = self.current_endurance

        quantity = int(endurance_quantity / drink_object.degrees)
        endurance_quantity = quantity * drink_object.degrees
        if drink_object.quantity < quantity:
            quantity = drink_object.quantity
            endurance_quantity = quantity * drink_object.degrees
        drink_object.quantity -= quantity
        self.current_endurance -= endurance_quantity

        msg = '{0} drinks {1} grams of {2}'.format(self.name, quantity, drink_object.name)
        logging.info(msg)
        self.party.messages.append(msg)
        self.try_change_state()
        return 1

    def endurance_percent(self):
        return round(self.current_endurance / self.endurance, 2)

    def try_change_state(self):
        percent = self.endurance_percent()
        if percent >= Drinker.STATE_FUNNY_PERCENT[0] and percent <= Drinker.STATE_FUNNY_PERCENT[1]:
            if random.random() <= Drinker.STATE_FUNNY_PERCENT[1] - Drinker.STATE_FUNNY_PERCENT[0]:
                self.state = Drinker.STATE_FUNNY
                self.party.messages.append('{0} change_state to {1}'.format(self.name, Drinker.STATE_NAMES[self.state]))
                return

        if percent >= Drinker.STATE_OUT_PERCENT[0] and percent <= Drinker.STATE_OUT_PERCENT[1]:
            if random.random() <= Drinker.STATE_OUT_PERCENT[1] - Drinker.STATE_OUT_PERCENT[0]:
                self.state = Drinker.STATE_OUT
                self.party.messages.append('{0} change_state to {1}'.format(self.name, Drinker.STATE_NAMES[self.state]))
                return

    def to_client(self):
        return {
            'name': self.name,
            'endurance': self.endurance,
            'current_endurance': self.current_endurance,
            'state': self.state
        }