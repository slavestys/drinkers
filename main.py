from twisted.web import server
from twisted.internet import reactor

from controllers.party_resource import PartyResource

site = server.Site(PartyResource())
reactor.listenTCP(8080, site)
reactor.run()
