import json
import threading
import logging

from twisted.web import resource

from controllers.party_controller import PartyController


class PartyResource(resource.Resource):
    isLeaf = True
    lock = threading.Lock()

    CONTROLLERS = {
        'party': PartyController
    }

    def render_GET(self, request):
        logging.info('Request got: {0}'.format(request.uri))
        path_array = request.path.decode('utf-8').split('/')
        controller_name = path_array[1]
        controller = PartyResource.CONTROLLERS.get(controller_name) if controller_name else PartyController
        if controller:
            action = path_array[2] if len(path_array) > 2 else None
            with PartyResource.lock:
                result = controller.invoke(action, request.args)
        else:
            error = 'unknown_controller'
            logging.error('unknown_controller')
            result = json.dumps({'errors': ['unknown_controller']})
        return result.encode('utf-8')