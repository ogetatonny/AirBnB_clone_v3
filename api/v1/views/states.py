#!/usr/bin/python3
<<<<<<< HEAD

""" create a new view for state objs(handles all default RESTFUL API"""

# import the needed modules

from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage

# Route for retrieving all state objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all state objects"""
    # Get from the storage all the state objs
    states = storage.all(State).values()
    # convert objs to dictionaries and jsonify the list
    state_list = [state.to_dict() for  state in states]
    return jsonify[state_list]

# rout for retrieving a specific state by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getz_states(state_id):
    """ Retrieves a State obj"""
    # Get the State obj with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # return the state obj in JSON format
        return jsonify(state.to_dict())
    else:
        # return 404 error if the State obj is not found
        abort(404)
# rout for deleting a specific State obj by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object"""
    # Get the state object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # delete the State object from the storage and save the changes
        storage.delete(state)
        storage.save()
        # return an empty JSON with 200 status code
        return jsonify (()), 200
    else:
        # return 404 error if the state object is not found
        abort(404)

# rout for creating a new state object
@app_views.route('/states', methods=[POST], strict_slashes=False)
def create_state():
    """Creates a State object"""
    if not request.get_json():
        # return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

        # get the JSON data from the request
        kwargs = request.get_json()
        if 'name' not in kwargs:
            # return 400 error if "name" key is missing in the JSON data
            abort(400, 'Missing name')
        # create a new State object with the JSON data
        state = state(**kwargs)
        # save the State object to the storage
        state.save()
        # return the newly created state object in JSON format with 201 status code
        return jsonify(state.to_dict()), 201

# route forupdating an existing State obj by ID
@app_views.route('/states/<state_id>', methods=[PUT], strict_slashes=False)
def update_states(state_id):
    """ Updated the state object"""
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if states:
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a Json')
        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update the attributes of the State object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        # save the updated state object to the storage
        state.save()
        # Return the updated state object in JSON format with 200 status code
        return jsonify(state.to_dict()), 200
    else:
        # Return 404 error if the state object is not found
        abort(404)

# Error handlers
@app_views.errorhandler(400)
def bad_request(error):
    """ Returns a bad request message for illegal requests to the API"""
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
=======
""" The  `app_views` blueprint for URI subpaths connected to `State` objects.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'],
                 strict_slashes=False)
def GET_all_State():
    """ JSON list containing `State` instance that is stored

    Return:
        All instances of `State` in a JSON list
    """
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def GET_State(state_id):
    """ Returns the id of the `State` instance stored in URI subpath.

    Args:
        state_id: uuid of the stored `State` instance

    Return:
        404 error response or instance of `State` with matching uuid
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_State(state_id):
    """ Removes storage instance of `State` by id in URI subpath

    Args:
        state_id: uuid of `State` instance in storage

    Return:
        Responds 200 or 404 if error and an empty dictionary
    """
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_State():
    """ Builds a fresh instance of `State` in storage

    Return:
        Responds 200 or 404 if error and an empty dictionary
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in req_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    new_State = State(**req_dict)
    new_State.save()

    return (jsonify(new_State.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_State(state_id):
    """ updates the storage instance of `State` by using the
    id in URI subpath and kwargs from the HTTP body request.

    Args:
        state_id: the storage based uuid of `State` instance

    Return:
        Dictionary empty and response status 200, or 404 if
    an error
    """
    state = storage.get(State, state_id)
    req_dict = request.get_json()

    if state:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return (jsonify(state.to_dict()))
    else:
        abort(404)
>>>>>>> 32f971af754391d0ddcb1a44afeabc3364a8eed4
