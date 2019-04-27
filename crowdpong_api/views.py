

import logging; log = logging.getLogger(__name__)
DEBUG = log.debug; INFO = log.info; WARN = log.warning; ERROR = log.error

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPMethodNotAllowed


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


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'crowdpong-api'}


@view_config(route_name='controller', renderer='json')
class ControllerAPI(BaseView):

    def get(self):
        sess = self.request.session
        count = sess.setdefault("count", 0)
        sess["count"] = count+1
        return {
            'team': sess.get('team', "unknown"),
            'paddle': 0.0, 
            'count': count
        }

    def post(self):
        command = self.request.json.get("command")
        return {'team': "blue", 'paddle': 0.0, 'command': command}


@view_config(route_name='game_state', renderer='json')
def game_state_api(request):
    return {'blue_paddle': 0.0, 'red_paddle': 0.0}


@view_config(route_name='game_config', renderer='json')
def game_config_api(request):
    return {'blue_paddle': 0.0, 'red_paddle': 0.0}

