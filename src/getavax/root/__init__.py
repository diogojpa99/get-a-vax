
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.view import view_config



@view_config(route_name='root.redirect', renderer='json')
def root(request):
  return HTTPSeeOther(location='/c/login')



def main(global_config, **settings):

  import logging, sys
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  for h in root.handlers:
    root.removeHandler(h)
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  root.addHandler(handler)

  config = Configurator()
  config.add_route('root.redirect', '/')
  config.scan('.')

  return config.make_wsgi_app()


# vi: set ts=2 sw=2 et : 
