#!/usr/bin/python3
"""
New view for State objects that handles taht handles all default ResFul API.
"""


from flask import abort
from flask import jsonify
from models.place import Place
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Obtain all cities and places
    """
    places_city = []
    if city_id is None:
        abort(404)
    if storage.get('City', city_id) is None:
        abort(404)
    for place in storage.get('City', city_id).places:
        places_city.append(place.to_dict())
    return jsonify(places_city)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_places_id(place_id):
    """
    obtain object places by it's id
    """
    placeArr = storage.get("Place", place_id)
    if placeArr is None:
        abort(404)
    return jsonify(placeArr.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_place_delete(place_id):
    """
    Deletes an object
    """
    DelArr = storage.get('Place', place_id)
    if DelArr is None:
        abort(404)
    else:
        storage.delete(DelArr)
        storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def set_places_POST(city_id):
    """
    Creates a new object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400

    user_post = storage.get('User', request.json['user_id'])
    if not user_post:
        abort(404)
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    n_place = Place(user_id=request.json["user_id"],
                    name=request.json["name"])
    n_place.city_id = city_id
    storage.new(n_place)
    storage.save()
    return jsonify(n_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def user_put_place(place_id):
    '''
    Inserts a new item to an object
    '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for atrr, value in request.get_json().items():
        if atrr not in ['id', 'created_at', 'updated_at']:
            setattr(place, atrr, value)
    storage.save()
    return jsonify(place.to_dict()), 200


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
