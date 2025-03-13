from flask import Blueprint, render_template, request, redirect, url_for
from webcrawler.utils import scrape_page  # Assuming you have a scrape_page function

bp = Blueprint("webui", __name__, template_folder="templates")

def index():
    """
    Handles the main page, displaying the form to enter a URL to scrape.
    If a URL is submitted, it initiates the scraping and displays results.
    """

    data = None  # Initialize data to None
    url = None   # Initialize url to None

    if request.method == "POST":
        target_url = request.form["target_url"]
        url = target_url  # Set url to the target URL
        data = scrape_page(target_url)  # Call your scraping function

    return render_template("index.html", data=data, url=url)

def results():
    """
    Displays the results of the last scraping, if any.
    This is a basic example; you might want to store results more persistently.
    """
    #  In a real application, you might want to store scraped data
    #  in a database or other storage, and retrieve it here.
    #  This is a placeholder to show the concept.
    return "This page would display the latest scraping results."

bp.add_url_rule("/", view_func=index, methods=["GET", "POST"])
bp.add_url_rule("/results", view_func=results)

def init_app(app):
    app.register_blueprint(bp)