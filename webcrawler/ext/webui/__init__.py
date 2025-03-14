from flask import Blueprint, render_template, request, redirect, url_for
from webcrawler.utils import scrape_page  # Assuming you have a scrape_page function
from . import views  # Import the views module

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=views.index, methods=["GET", "POST"])
bp.add_url_rule("/page/<int:page_id>", view_func=views.page)

def init_app(app):
    app.register_blueprint(bp)