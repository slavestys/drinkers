from twisted.web import server
from twisted.internet import reactor

from party_server import PartyServer

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