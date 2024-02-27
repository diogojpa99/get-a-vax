import datetime
import json

# flask debug on
# export FLASK_ENV=development

### pip install flask
### python app.py

from flask import (
    Flask, request
)



def create_app(*args, **kwargs):
  app = Flask(__name__)

  @app.route('/ping', methods=('GET',))
  def ping():
    return { 'pong':True }

  @app.route('/disponibilidade', methods=('GET',))
  def disponibilidade():
    rvalue = {}
    _from = datetime.datetime.fromisoformat(request.args['desde'])
    to = datetime.datetime.fromisoformat(request.args['a'])
    ctx = request.args['centro']
    j = """{ }"""
    
    with open('disponibilidade.json', 'r') as f:# read json file
      j = f.read()
      
    return j

  @app.route('/reserva', methods=('POST',))
  def reserva():
    
    if not request.data:
      raise Exception('no body')
    body = request.get_json()
    
    with open('reserva-error.json', 'r') as f: # read json file
      j = f.read()
      if body['centro'] == '32fcfe73-bf1a-4e7e-b729-6578b7d3b08e': # If the center equals some particular id then it will give an error
        return j
      else:
        with open('reserva-ok.json', 'r') as f: # read json file
          i = f.read()
          return i
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
