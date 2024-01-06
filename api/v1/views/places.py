#!/usr/bin/python3
""" Creates a view for Place objects - handles all default RESTFUL API actions"""

# import the needed modules
from flask import abort, jsonify, request
# import the required models
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage

# route for retrieving all Place objects of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """ retrieves the list of all Place objects of a City"""
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if the City object is not found
        abort(404)
        
    # Get all place objects of the city and convert them to dictionaries
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

# Route for retrieving a specific Place object by ID
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object"""
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
    """ Deletes a Place object"""
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Deletes the Place object from the storage and save changes
        storage.delete(place)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Place object is not found
        abort(404)

# Route for creating a new Place object
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object"""
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
        # Return 400 error if 'name'key is missing in the JSON data
        abort(400, 'Missing name')

    # Get the User object with the given user_id from the storage
    user = storage.get(User, data['user_id'])
    if not user:
        # Return 404 error if the User object is not found
        abort(404)

    # Assign the city_id to the JSON data
    data['city_id'] = city_id

    # Create a new place object with the JSON data
    place = place(**data)
    # Save the Place object to the storage
    place.save()
    # Return the newly created Place object in JSON format with 201 status code
    return jsonify(place.to_dict()), 201

# Route for updating an existing Place object by ID
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a Place object"""
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created at', 'updated at']
       # update the attributes of the Place object with the JSON data
       for key, value in data.items():
           if key not in ignore_keys:
               setattr(place, key, value)

        # Save the updated Place object to the storage
        place.save()
        # Return the updated Place object to the storage
        return jsonify(place.to_dict()), 200
    else:
        # Return 404 error if the Place object is not found
        abort(404)

# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """ Returns 404: Not Found"""
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """ Return Bad Request message for illegal request to the API"""
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

# task 15
# New endpoint: POST /api/v1/places_search
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ Retrieves Place objects based on the provided JSN search criteria"""
    # check if the request contains valid JSON
    if request.get_json() is None:
        abort(400, description="Not a JSON")
    # Extract data from the JSON request body
    data = request.get_json()
    # Extract criteria from the data
    if data and len(data):
        # Extract the 'states' criteria from the JSON data
        states = data.get('states', None)
        # Extract the 'cities' criteria from the JSON data
        cities = data.get('cities', None)
        # Extract the 'amenities' criteria from the JSON data
        amenities = data.get('amenities', None)

    # If no criteria provided, retrieve all places
    if not data or not len(data) or (not states and not cities and not amenities):
        # Retrieve all Place objects from storage
        places = storage.all(place).values()
        # create a list to store the converted dictionaries of places
        list_places = []
        # convert each place object to a dictionary and append to the list
        for place in places:
            list_places.append(place.to_dict())
        # Return the list of places in JSON format
        return jsonify(list_places)

    # Create a list to store filtered places based on criteria
    list_places = []

    # Filter and retrieve places based on states criteria
    if states:
        # Retrieve state objects corresponding to the provided state IDs
        state_obj = [storage.get(State, s_id) for s_id in states]
        # iterate through each state object
        for state in states_obj:
            # check if the State object exists
            if state:
                # Iterates through each city in the State's cities list
                for city in state.cities:
                    # check the City object exists
                    if city:
                        # iterates through each place in the City's places list
                        for place in city.places:
                            # Append the place to the list of filteredplaces
                            list_places.append(place)

    # filter and retrieve places based on cities criteria
    if cities:
        # retrieve City objects corresponding to the provided city IDs
        city_obj = [storage.get(city, c_id) for c_id in cities]
        # iterates through each City object
        for city in city_obj:
            # check if the city object exists
            if city:
                # iterates through each place in the City's places list
                for place in city.places:
                    # check if the place is not already in the lst
                    if place not in list_places:
                        # append the Place to the list of filtered places
                        list_places.append(place)

    # filter places based on amenities criteria
    if amenities:
        # if list_places is empty, retrieve all place objects from storage
        if not list_places:
            list_places = storage.all(Place).values()
        # Retrieve Amenity objects corresponding to the provided amenity IDs
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        # filter the list of places based on whether they have all specified amenities
        list_places = [place for place in list_places if all([am in place.amenities for am in amenities_obj])]

    # prepare the final list of places for response
    places = []
    # iterates through the list of filtered places
    for p in list_places:
        # convert the place object to a dictionary
        d = p.to_dict()
        # remove the 'amenities' key from the dictionary
        d.pop('amenities', None)
        # append the modified dictionary to the 'places' list
        places.append(d)

    # Return the list of places in JSON format
    return jsonify(places)
