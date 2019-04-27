

import logging; log = logging.getLogger(__name__)
DEBUG = log.debug; INFO = log.info; WARN = log.warning; ERROR = log.error


class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        method = self.request.method.lower()
        f = getattr(self, method, None)
        if f:
            return f()

        WARN("no method %s on %s" % (method, self))
        raise HTTPMethodNotAllowed

    # allow CORS pre-flight, headers are added in NewResponse event handler
    def options(self):
        return Response()
