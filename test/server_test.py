import json
import threading
from multiprocessing import Process

from mock import patch
from twisted.trial import unittest

from test.support.dummy_site import DummySite
from controllers.party_resource import PartyResource
from controllers.party_controller import PartyController
from models.party import Party


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.web = DummySite(PartyResource)
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

    def test_party_hard(self):
        self.web.get("/party/add_drink?name=whisky&degrees=40&quantity=400")
        self.web.get("/party/add_drinker?name=misha&endurance=20000")
        with patch('random.random') as random_mock:
            random_mock.return_value = 0.9
            response = self.web.get("/party/party_hard")
        value = json.loads(response.value())
        self.assertEqual(value['state'], Party.STATE_BAD_END)
        self.assertEqual(value['drinks'], [])
        self.assertEqual(value['drinkers'][0]['current_endurance'], 4000)

        response = self.web.get("/party/party_clean")
        value = json.loads(response.value())
        self.assertEqual(value, self.expect)

        self.web.get("/party/add_drink?name=whisky&degrees=40&quantity=400")
        self.web.get("/party/add_drinker?name=misha&endurance=20000")
        with patch('random.random') as random_mock:
            random_mock.return_value = 0.1
            response = self.web.get("/party/party_hard")
        value = json.loads(response.value())
        self.assertEqual(value['state'], Party.STATE_GOOD_END)

    def test_concurrency(self):
        self.web.get("/party/add_drink?name=whisky&degrees=40&quantity=400")
        self.web.get("/party/add_drinker?name=misha&endurance=20000")
        test_case = self
        test_case.concurrency_checked = 0

        def clean_party():
            test_case.web.get("/party/party_clean")
            test_case.concurrency_checked = 1

        thread = threading.Thread(target=clean_party)

        class PartyControllerMocked(PartyController):

            @staticmethod
            def mocked_invoke(method, parameters):
                invoke_patch.stop()
                thread.start()
                return PartyController.invoke(method, parameters)

        invoke_patch = patch.object(PartyController, 'invoke', wraps=PartyControllerMocked.mocked_invoke)
        invoke_patch.start()
        with patch('random.random') as random_mock:
            random_mock.return_value = 0.9
            response = self.web.get("/party/party_hard")
            value = json.loads(response.value())
            self.assertEqual(value['state'], Party.STATE_BAD_END)

        thread.join()
        self.assertTrue(test_case.concurrency_checked)


