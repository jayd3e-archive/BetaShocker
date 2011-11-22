from pyramid.config import Configurator
from betashock.resources import RootResource

def main(global_config, **settings):
        '''Main config function'''
        config = Configurator(settings=settings,
                              root_factory=RootResource)
         
        config.add_static_view(name='static', path='betashock:static')

        #Handler Root Routes
        config.add_route("index", "/")

        config.scan()
        return config.make_wsgi_app()

if __name__ == '__main__':
    from paste.httpserver import serve
    serve(main(), host="0.0.0.0", port="5000")
