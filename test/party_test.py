import unittest

from models.party import Party
from models.drinker import Drinker
from models.drink import Drink
from test.support.test_helper import CleanUp


class PartyTest(unittest.TestCase):
    def setUp(self):
        self.party = Party()
        self.party.add_drinker(Drinker('Misha', 20000))
        self.party.add_drinker(Drinker('Slava', 20000))
        self.addCleanup(CleanUp.clean_up)

    def test_party_bad_end(self):
        drink = Drink('Whisky', 40, 400)
        self.party.add_drink(drink)
        self.party.party_hard()
        self.assertEqual(self.party.state, Party.STATE_BAD_END)

    def test_party_goof_end(self):
        drink = Drink('Whisky', 40, 4000)
        self.party.add_drink(drink)
        self.party.party_hard()
        self.assertEqual(self.party.state, Party.STATE_GOOD_END)

    def test_save_and_load(self):
        drink = Drink('Whisky', 40, 4000)
        self.party.add_drink(drink)
        self.party.save()

        other_instance = Party.load()
        self.assertEqual(other_instance.drinks[0].name, 'Whisky')