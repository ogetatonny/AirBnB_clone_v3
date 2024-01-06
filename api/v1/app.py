#!/usr/bin/python3
<<<<<<< HEAD
""" Creates flask app and registers the blueprint app_views with the Flask instance 'app'."""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# task 12
# enable CORS and allow requests from any origin:
CORS(app, reources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# Register the app_views blueprint:
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Teardown function to close the SQLAlchemysession object after each request:
@app.teardown_appcontext

def teardown_engine(exception):
    """ Removes the SQLAlchemy session after each request."""
    storage.close()

# task 5
# Error handler for 404 Not Found:
@app.errorhandler(404)
def not_found(error):
    """Return JSON response with "Not found" error message"""
    response = {'error': 'Not found'}
    return jsonify(response), 404

if __name__ == '__main__':
    #get the host and port from environment variables.
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    # Run the app in threaded mode for better performance
    app.run(host=HOST, port=PORT, threaded=True)
=======
"""Create an api"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """Dismantling technique"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors

    args:
        state of errors
    return:
        JSON error message
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host, port, threaded=True)
>>>>>>> 32f971af754391d0ddcb1a44afeabc3364a8eed4
