import logging
import logging.config

from twisted.web import server
from twisted.internet import reactor

from controllers.party_resource import PartyResource
from application import Application

Application.load_config()
logging.config.dictConfig(Application.config['logger'])
logging.getLogger('root').info('Start')

site = server.Site(PartyResource())
reactor.listenTCP(Application.port(), site)
reactor.run()
