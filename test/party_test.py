import unittest

from models.party import Party
from models.drinker import Drinker
from models.drink import Drink


class PartyTest(unittest.TestCase):
    def setUp(self):
        self.party = Party()
        self.party.add_drinker(Drinker('Misha', 20000))
        self.party.add_drinker(Drinker('Slava', 20000))

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