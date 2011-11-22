from deform import Form
from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.exceptions import Forbidden
from betashock.utils import mako_form_renderer
from betashock.handlers.exceptions import notFound
from betashock.handlers.exceptions import forbidden
from betashock.models.base import initializeBase
from betashock.resources.root import RootResource
from betashock.request import BetaShockRequest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine_from_config

def main(global_config, **settings):
        '''Main config function'''
        engine = engine_from_config(settings, 'sqlalchemy.')
        initializeBase(engine)
        maker = sessionmaker(bind=engine)
        settings['db.sessionmaker'] = maker
        
        config = Configurator(settings=settings,
                              root_factory=RootResource)
         
        config.add_static_view(name='static', path='betashock:static')

        #Includes
        config.include('pyramid_tm')
        
        #Handler Root Routes
        #Handler Action Routes
                                                                                                            
        #Exception Views
        config.add_view(notFound,
                        context=NotFound,
                        permission='__no_permission_required__',
                        renderer='exceptions/not_found.mako')

        config.add_view(forbidden,
                        context=Forbidden,
                        permission='__no_permission_required__')

        return config.make_wsgi_app()

if __name__ == '__main__':
    from paste.httpserver import serve
    serve(main(), host="0.0.0.0", port="5432")
