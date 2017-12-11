import logging
import logging.config

from twisted.web import server
from twisted.internet import reactor

from controllers.party_resource import PartyResource
from application import Application

Application.init()
logging.info('Start')

site = server.Site(PartyResource())
reactor.listenTCP(Application.port(), site)
reactor.run()
