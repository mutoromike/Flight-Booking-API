""" app/events/views.py """

from functools import wraps
from flask import Flask, request, jsonify, abort, make_response, g
from flask.views import MethodView
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url

from . import image_blueprint
from app.models.models import User, Images
from app.helpers.auth import authorize

import re


class ProcessImages(MethodView):
    """
        This class handles image processing
            Uploading
            Changing
    """
    @authorize
    def post(self, user_id, current_user):
        """
        POST method to upload image to
        remote server and save image url
        to the DB
        """
        data = request.get_json()
        response = upload(data["image_url"], public_id=user_id)
        user = Images.query.filter_by(user=user_id).first()
        if user:
            response = {
                "message": "You already have a passport uploaded, " \
                "to change the photo kindly delete the current one before uploading " \
                "a new passport photo"
            }
            return make_response(jsonify(response)), 400
        else:
            # Create image url
            url, options = cloudinary_url(
                response['public_id'],
                format=response['format'],
                width=250,
                height=250,
                gravity="faces",
                crop="fill"
            )

            try:
                new_image = Images(
                    image_url=url,
                    user=user_id
                )
                new_image.save()
                response = { 'message': "Passport has been uploaded successfully" }
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = { 'message': str(e) }
                return make_response(jsonify(response)), 500

    @authorize
    def get(self, user_id, current_user):
        """
        Method to get the client's passport url
        """
        image = Images.query.filter_by(user=user_id).first()
        response = {
            "image_url": image.image_url
        }
        return make_response(jsonify(response)), 200

    @authorize
    def delete(self, user_id, current_user):
        """
        Method to delete a client's passport url
        """
        image = Images.query.filter_by(user=user_id).first()
        # image_url = image.image_url
        try:
            destroy(str(user_id))
            image.delete()
            response = {"message": "Passport successfully deleted"}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"message": str(e)}
            return make_response(jsonify(response)), 500
    

images_view = ProcessImages.as_view('images')

image_blueprint.add_url_rule('/api/v1/image', view_func=images_view)
