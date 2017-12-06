import json

from twisted.trial import unittest

from support.dummy_site import DummySite
from party_server import PartyServer
from party_controller import PartyController
from party import Party


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.web = DummySite(PartyServer)
        self.expect = {
            "drinkers": [],
            "drinks": [],
            "state": 1
        }

    def tearDown(self):
        PartyController.party = Party()

    def test_first_request(self):
        response = self.web.get("/")
        value = json.loads(response.value())
        self.assertEqual(value, self.expect)

    def test_add_drink(self):
        response = self.web.get("/party/add_drink?name=whisky&degrees=40&quantity=500")
        value = json.loads(response.value())
        self.expect['drinks'].append({
            'name': 'whisky',
            'degrees': 40,
            'quantity': 500
        })
        self.assertEqual(value, self.expect)

    def test_add_drinker(self):
        response = self.web.get("/party/add_drinker?name=misha&endurance=20000")
        value = json.loads(response.value())
        self.expect['drinkers'].append({
            'name': 'misha',
            'current_endurance': 20000,
            'endurance': 20000,
            'state': 1
        })
        self.assertEqual(value, self.expect)

