from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest


class SmartDummyRequest(DummyRequest):

    def __init__(self, method, url, args = None):
        DummyRequest.__init__(self, url)
        self.method = method
        splitted_url = url.split('?')
        self.path = (splitted_url[0] or '/').encode('utf-8')

        args = args or {}
        if len(splitted_url) > 1:
            for var in splitted_url[1].split('&'):
                splitted_var = var.split('=')
                if len(splitted_var) > 1:
                    args[splitted_var[0].encode('utf-8')] = splitted_var[1].encode('utf-8')

        for k, v in args.items():
            self.addArg(k, v)

    def value(self):
        return ''.join(list(map(lambda x: x.decode('utf-8'), self.written)))


class DummySite(server.Site):
    def get(self, url):
        return self._request("GET", url)

    def post(self, url, args=None):
        return self._request("POST", url, args)

    def _request(self, method, url, args = None):
        request = SmartDummyRequest(method, url, args)
        resource = self.getResourceFor(request)()
        result = resource.render(request)
        return self._resolveResult(request, result)

    def _resolveResult(self, request, result):
        request.write(result)
        request.finish()
        succeed(request)
        return request
