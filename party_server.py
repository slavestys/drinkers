import json

from twisted.web import resource

from party_controller import PartyController


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