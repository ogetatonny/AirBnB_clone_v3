<<<<<<< HEAD
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.root('/status', methods-['GET'])
def api_status():
    """ Reutns the health of RESTFUL API through the Json response"""
    response - {'status': 'OK'}
    return jsonify(response)
# TASK 4
@app_views.root('/stats', methods-['GET'])
def get_stats():
    """ Retrieves the no of each objs by type"""
    stats - {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
=======
#!/usr/bin/python3
"""view index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from collections import OrderedDict

class_plurals = {'amenities': Amenity, 'cities': City, 'places': Place,
                 'reviews': Review, 'states': State, 'users': User}


@app_views.route('/status', strict_slashes=False)
def status():
    """the state of the v1 API"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Itemized count of the objects stored in each class.

    """
    stats = OrderedDict()
    for key in sorted(class_plurals.keys()):
        count = storage.count(class_plurals[key])
        if count > 0:
            stats[key] = count
>>>>>>> 32f971af754391d0ddcb1a44afeabc3364a8eed4
    return jsonify(stats)
