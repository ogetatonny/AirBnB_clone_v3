#!/usr/bin/python3
'''
Create a view for Place objects - handles all default RESTful API actions
'''

# Import necessary modules
from flask import abort, jsonify, request
# Import the required models
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all Place objects of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    '''
    Retrieves the list of all Place objects of a City
    '''
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if the City object is not found
        abort(404)

    # Get all Place objects of the City and convert them to dictionaries
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


# Route for retrieving a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    '''
    Retrieves a Place object
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Return the Place object in JSON format
        return jsonify(place.to_dict())
    else:
        # Return 404 error if the Place object is not found
        abort(404)


# Route for deleting a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''
    Deletes a Place object
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Delete the Place object from the storage and save changes
        storage.delete(place)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Place object is not found
        abort(404)


# Route for creating a new Place object
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
    Creates a Place object
    '''
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if the City object is not found
        abort(404)

    # Check if the request data is in JSON format
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON data from the request
    data = request.get_json()
    if 'user_id' not in data:
        # Return 400 error if 'user_id' key is missing in the JSON data
        abort(400, 'Missing user_id')
    if 'name' not in data:
        # Return 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Get the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Return 404 error if the User object is not found
        abort(404)

    # Assign the city_id to the JSON data
    data['city_id'] = city_id
    # Create a new Place object with the JSON data
    place = Place(**data)
    # Save the Place object to the storage
    place.save()
    # Return the newly created Place object in JSON format with 201 status
    return jsonify(place.to_dict()), 201


# Route for updating an existing Place object by ID
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Updates a Place object
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        # Update the attributes of the Place object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        # Save the updated Place object to the storage
        place.save()
        # Return the updated Place object in JSON format with 200 status code
        return jsonify(place.to_dict()), 200
    else:
        # Return 404 error if the Place object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found
    '''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to the API
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400


# New endpoint: POST /api/v1/places_search
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves Place objects based on the provided JSON search criteria
    """

    # Check if the request contains valid JSON
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    # Extract data from the JSON request body
    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    # If no criteria provided, retrieve all places
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []

    # Filter and retrieve places based on states criteria
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    # Filter and retrieve places based on cities criteria
    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    # Filter places based on amenities criteria
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    # Prepare the final list of places for response
    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    # Return the list of places in JSON format
    return jsonify(places)

api/v1/views/places_amenities.py

#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Place - Amenity """


from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object of a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)

api/v1/views/places_reviews.py

#!/usr/bin/python3
'''
Create a new view for Review objects - handles all default RESTful API
'''

# Import necessary modules
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


# Route for retrieving all Review objects of a Place
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    '''
    Retrieves the list of all Review objects of a Place
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if the Place object is not found
        abort(404)

    # Get all Review objects of the Place and convert them to dictionaries
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


# Route for retrieving a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''
    Retrieves a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Return the Review object in JSON format
        return jsonify(review.to_dict())
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Route for deleting a specific Review object by ID
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''
    Deletes a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Delete the Review object from the storage and save changes
        storage.delete(review)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Route for creating a new Review object
@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    Creates a Review object
    '''
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if the Place object is not found
        abort(404)

    # Check if the request data is in JSON format
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON data from the request
    data = request.get_json()
    if 'user_id' not in data:
        # Return 400 error if 'user_id' key is missing in the JSON data
        abort(400, 'Missing user_id')
    if 'text' not in data:
        # Return 400 error if 'text' key is missing in the JSON data
        abort(400, 'Missing text')

    # Get the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Return 404 error if the User object is not found
        abort(404)

    # Assign the place_id to the JSON data
    data['place_id'] = place_id
    # Create a new Review object with the JSON data
    review = Review(**data)
    # Save the Review object to the storage
    review.save()
    # Return the newly created Review object in JSON format with 201 status
    return jsonify(review.to_dict()), 201


# Route for updating an existing Review object by ID
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Updates a Review object
    '''
    # Get the Review object with the given ID from the storage
    review = storage.get(Review, review_id)
    if review:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        # Update the attributes of the Review object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        # Save the updated Review object to the storage
        review.save()
        # Return the updated Review object in JSON format with 200 status code
        return jsonify(review.to_dict()), 200
    else:
        # Return 404 error if the Review object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found
    '''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to the API
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
