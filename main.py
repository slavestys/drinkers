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
        parh_array = request.path.decode('utf-8').split('/')
        controller_name = parh_array[1]
        controller = PartyServer.CONTROLLERS[controller_name]
        action = parh_array[2]

        return controller.invoke(action, request.args).encode('utf-8')

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