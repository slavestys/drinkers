import json

from twisted.web import server, resource
from twisted.internet import reactor

from party_controller import PartyController
from drink import Drink
from drinker import Drinker
from party import Party



class PartyServer(resource.Resource):
    isLeaf = True

    CONTROLLERS = {
        'party': PartyController
    }

    def render_GET(self, request):
        path_array = request.path.decode('utf-8').split('/')
        controller_name = path_array[1]
        controller = PartyServer.CONTROLLERS.get(controller_name) if controller_name else PartyController
        if controller:
            action = path_array[2] if len(path_array) > 2 else None
            result = controller.invoke(action, request.args)
        else:
            result = json.dumps({'errors': ['unknown_controller']})
        return result.encode('utf-8')

site = server.Site(PartyServer())
reactor.listenTCP(8080, site)
reactor.run()

# drinkers = [
#     Drinker('Slava', 20000),
#     Drinker('Misha', 20000)
# ]
#
# drinks = [
#     Drink('Whisky', 40, 500),
#     Drink('Cognac', 40, 500)
# ]
#
# party = Party(drinkers, drinks)
# party.party_hard()