import unittest
import random

from mock import patch

from models.party import Party
from models.drinker import Drinker
from models.drink import Drink


class DrinkerTest(unittest.TestCase):

    def test_one_drink(self):
        party = Party()
        drinker = Drinker('Misha', 20000)
        party.add_drinker(drinker)
        drink = Drink('Whisky', 40, 400)

        def mock_randint_method(_, max):
            return max

        with patch('random.randint', side_effect=mock_randint_method), patch('random.random') as random_mock:
            random_mock.return_value = 0.2

            drinker.drink(drink)
            self.assertEqual(drinker.current_endurance, 10000)
            self.assertEqual(drinker.state, Drinker.STATE_FUNNY)
            self.assertEqual(drink.quantity, 150)

            drinker.drink(drink)
            self.assertEqual(drinker.current_endurance, 10000)
            self.assertEqual(drink.quantity, 150)

            drinker.state = Drinker.STATE_NORMAL
            drinker.drink(drink)
            self.assertEqual(drinker.current_endurance, 4000)
            self.assertEqual(drink.quantity, 0)
            self.assertEqual(drinker.state, Drinker.STATE_OUT)