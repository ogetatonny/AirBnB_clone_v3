<<<<<<< HEAD
#!/usr/python3
""" creates a view for Amenity objects - handles all default RESTFUL API actions"""

# import the needed modules
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import storage

# route for retrieving all Amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    # Get all Amenity objects from the storage
    amenities = storage.all(Amenity).values()
    # convert objects to dictionaries and jsonify the list
    return jsonify([amenity.to_dict() for amenity in amenities])

# route for retrieving a specific Amenity object by Id
@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object"""
    # Get the Amenity object with the given id from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return the Amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # return 404 error if the Amenity object is not found 
        abort(404)

# route for deleting a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity9amenity_id):
    """ Deletes an amenity object"""
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Delete the Amenity object from the storage and save changes
        storage.delete(amenity)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # return 404 error if the Amenity object is not found
        abort(404)

# Route for creating a new Amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity object"""
    if not request.get_json():
        # Return 400 error if the request data is not found in JSON format
        abort(400, 'Not a JSON')
        # Get the JSON data from  the request
        data = request.get_json()
        if 'name' not in data:
            # Return 400 error if 'name' key is missing in the JSON data
            abort(400, 'Missing name')
        # creates a new Amenity object with the JSON data
        amenity = Amenity(**data)
        # save the Amenity object to the storage
        amenity.save()
        # Return the newly created Amenity
        # object in JSON format with 201 status code
        return jsonify(amenity.to_dict()), 201

# Route for updating an existing Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates Amenity object"""
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return 400 error if the request data is not in JSON format
        if not request.get_json():
            abort(400, 'Not a JSON')
        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created at', 'updated at']
        # update the attributes of the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        # Save the updated Amenity object to the storage
        amenity.save()
        # Return the updated Amenity object in JSON format with 200 status code
        return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if the Amenity object is not found
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
    """ Return Bad Request message for illegal requests to the API"""
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
=======
#!/usr/bin/python3
""" Flask routes utilizing the  `app_views` Blueprint for
URI subpaths associated to `Amenity` objects.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
def GET_all_Amenity():
    """ Provides JSON list of storage-based `Amenity` instance.

    Return:
        All instances of `Amenity` in a JSON list
    """
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Amenity(amenity_id):
    """ Returns the storage instance of `Amenity` via URI subpath id.

    Args:
        amenity_id: The storage-based uuid of the `Amenity` instance

    Return:
        A 404 error message or an instance of `Amenity` with
    the matching uuid
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Amenity(amenity_id):
    """ URI subpath id Deletes `Amenity` object in storage

    Args:
        amenity_id: uuid of the stored instance of `Amenity`

    Return:
        Dictionary empty and response status 200
    or 404 in the event of an error.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def POST_Amenity():
    """ Generates a fresh instance of `Amenity` in storage

    Return:
        Dictionary empty and response status 200, or
    404 in the event of an error
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in req_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    new_Amenity = Amenity(**req_dict)
    new_Amenity.save()

    return (jsonify(new_Amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_Amenity(amenity_id):
    """ Modifies `Amenity` object in storage using the id in the 
    URI subpath and arguments from HTTP body request JSON dict.

    Args:
        amenity_id: Storage based uuid of the `Amenity` instance

    Return:
        Dictionary empty and response status 200
    or 404 in the event of an error
    """
    amenity = storage.get(Amenity, amenity_id)
    req_dict = request.get_json()

    if amenity:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return (jsonify(amenity.to_dict()))
    else:
        abort(404)
>>>>>>> 32f971af754391d0ddcb1a44afeabc3364a8eed4
