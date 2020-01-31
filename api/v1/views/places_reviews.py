#!/usr/bin/python3
"""
New view for CIty objects that handles taht handles all default ResFul API.
"""


from flask import abort
from flask import jsonify
from models.review import Review
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """
    Retrieves a list of review
    """
    if place_id is None:
        abort(404)
    review_list = []
    if storage.get('Place', place_id) is None:
        abort(404)
    get_reviews = storage.all("Review")
    for key, value in get_reviews.items():
        if value.place_id == place_id:
            review_list.append(value.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """
    Return id of the function
    """
    reviewArr = storage.get("Review", review_id)
    if reviewArr is None:
        abort(404)
    return jsonify(reviewArr.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_review_delete(review_id):
    """
    method Delete of the function
    """
    reviewArr = storage.get('Review', review_id)
    if reviewArr is None:
        abort(404)
    else:
        storage.delete(reviewArr)
        storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def set_review_POST(place_id):
    """
    Places object
    """
    place = storage.get("Place", place_id)
    info = request.get_json()
    user = storage.get("User", request.json["user_id"])
    if place is None:
        abort(404)
    if not info:
        abort((400), "Not a JSON")
    elif 'user_id' not in info:
        abort((400), "Missing user_id")
    elif user is None:
        abort(404)
    elif 'text' not in info:
        abort((400), "Missing text")
    else:
        info["place_id"] = place_id
        review_post = Review(**info)
        storage.new(review_post)
        storage.save()
        new_review = storage.get("Review", review_post.id)
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def set_review_PUT(review_id):
    """
    method PUT
    """
    review_st = storage.get("Review", review_id)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if review_st is None:
        abort(404)
    for atriv, val in request.json.items():
        if ((atriv != "id" and atriv != "place_id" and
             atriv != "created_at" and atriv != "updated_at" and
             atriv != "user_id")):
            setattr(review_st, atriv, val)
    storage.save()
    return jsonify(review_st.to_dict()), 200

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
