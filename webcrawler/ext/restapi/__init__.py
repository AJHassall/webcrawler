from flask import Blueprint
from flask_restful import Api

from .resources import PageItemResource, PageResource  # Assuming you've renamed your resources

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(PageResource, "/pages")  
    api.add_resource(PageItemResource, "/pages/<int:page_id>")
    app.register_blueprint(bp)