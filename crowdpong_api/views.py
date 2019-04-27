

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
        rs = self.request.redis_store

        data = dict(rs)
        data['team'] = sess.get('team', "unknown")
        return data

    def post(self):

        sess = self.request.session
        rs = self.request.redis_store
        command = self.request.json.get("command")

        paddle_v = "paddle_%s_v" % sess["team"]

        if command == "down":
            if rs[paddle_v] < rs["paddle_max_v"]:
                rs[paddle_v] += rs["paddle_delta_v"]
        elif command == "up":
            if rs[paddle_v] > -rs["paddle_max_v"]:
                rs[paddle_v] -= rs["paddle_delta_v"]
        elif command == "faster":
            rs['ball_v'] *= 1.1
        elif command == "slower":
            rs['ball_v'] *= 0.9
        else:
            raise ValueError("unknown command %s" % command)

        return {
            'team': sess["team"], 
            'command': command, 
            'paddle_v': rs[paddle_v],
        }


@view_config(route_name='game_state', renderer='json')
def game_state_api(request):
    rs = request.redis_store
    return dict(rs)


@view_config(route_name='game_config', renderer='json')
def game_config_api(request):
    return {'blue_paddle': 0.0, 'red_paddle': 0.0}

