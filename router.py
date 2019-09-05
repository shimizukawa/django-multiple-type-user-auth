import os

import bottle
from urllib.request import urlopen, install_opener, Request, HTTPError
from urllib.parse import urlparse, urlunparse

PORT = os.environ.get('PORT', 8080)


def opener_setup():
    from urllib.request import OpenerDirector, ProxyHandler, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, DataHandler
    opener = OpenerDirector()
    for klass in [ProxyHandler, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, DataHandler]:
        opener.add_handler(klass())
    install_opener(opener)


class Router:
    def __init__(self, proto, domain):
        self.proto = proto
        self.domain = domain

    def route(self, **paths):
        parts = urlparse(bottle.request.url)
        url = urlunparse((self.proto, self.domain) + parts[2:])
        try:
            method = bottle.request.method
            data = bottle.request.body
            req = Request(url, data=data, headers=bottle.request.headers, method=method)
            opener_setup()
            uo = urlopen(req)
            headers = uo.getheaders()
            new_headers = []
            for k,v in headers:
                if self.domain in v:
                    v = v.replace(self.domain, parts[1])
                new_headers.append((k, v))
            return bottle.HTTPResponse(uo.read(), status=uo.status, headers=dict(new_headers))
        except HTTPError as e:
            return bottle.HTTPResponse(e.reason, status=e.code, headers=dict(e.headers))


front = Router('http', 'localhost:8000')
admin = Router('http', 'localhost:8001')

@bottle.route('/admin', method='GET')
@bottle.route('/admin', method='POST')
@bottle.route('/admin/', method='GET')
@bottle.route('/admin/', method='POST')
@bottle.route('/admin/<path1>', method='GET')
@bottle.route('/admin/<path1>', method='POST')
@bottle.route('/admin/<path1>/', method='GET')
@bottle.route('/admin/<path1>/', method='POST')
@bottle.route('/admin/<path1>/<path2>', method='GET')
@bottle.route('/admin/<path1>/<path2>', method='POST')
@bottle.route('/admin/<path1>/<path2>/', method='GET')
@bottle.route('/admin/<path1>/<path2>/', method='POST')
@bottle.route('/admin/<path1>/<path2>/<path3>', method='GET')
@bottle.route('/admin/<path1>/<path2>/<path3>', method='POST')
@bottle.route('/admin/<path1>/<path2>/<path3>/', method='GET')
@bottle.route('/admin/<path1>/<path2>/<path3>/', method='POST')
@bottle.route('/admin/<path1>/<path2>/<path3>/<path4>', method='GET')
@bottle.route('/admin/<path1>/<path2>/<path3>/<path4>', method='POST')
@bottle.route('/admin/<path1>/<path2>/<path3>/<path4>/', method='GET')
@bottle.route('/admin/<path1>/<path2>/<path3>/<path4>/', method='POST')
def router1(**paths):
    return admin.route(**paths)


@bottle.route('/', method='GET')
@bottle.route('/', method='POST')
@bottle.route('/<path1>', method='GET')
@bottle.route('/<path1>', method='POST')
@bottle.route('/<path1>/', method='GET')
@bottle.route('/<path1>/', method='POST')
@bottle.route('/<path1>/<path2>', method='GET')
@bottle.route('/<path1>/<path2>', method='POST')
@bottle.route('/<path1>/<path2>/', method='GET')
@bottle.route('/<path1>/<path2>/', method='POST')
@bottle.route('/<path1>/<path2>/<path3>', method='GET')
@bottle.route('/<path1>/<path2>/<path3>', method='POST')
@bottle.route('/<path1>/<path2>/<path3>/', method='GET')
@bottle.route('/<path1>/<path2>/<path3>/', method='POST')
@bottle.route('/<path1>/<path2>/<path3>/<path4>', method='GET')
@bottle.route('/<path1>/<path2>/<path3>/<path4>', method='POST')
@bottle.route('/<path1>/<path2>/<path3>/<path4>/', method='GET')
@bottle.route('/<path1>/<path2>/<path3>/<path4>/', method='POST')
def router2(**paths):
    return front.route(**paths)


bottle.run(host='localhost', port=int(PORT), debug=True)

