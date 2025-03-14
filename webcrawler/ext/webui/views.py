from flask import abort, render_template, request
from flask_simplelogin import login_required
from webcrawler.models import Page, Link  # Import the Link model
from webcrawler.utils import scrape_page  # Assuming you have a scrape_page function


def index():
    """
    Handles the main page, displaying the form to enter a URL to scrape.
    If a URL is submitted, it initiates the scraping and displays results on the same page.
    Also displays all scraped links from the database.
    """
    data = None
    url = None

    if request.method == "POST":
        target_url = request.form["target_url"]
        url = target_url
        data = scrape_page(target_url)

    links = Link.query.all()  # Get all links from the database

    print(len(links))

    return render_template("index.html", data=data, url=url, links=links)

def page(page_id):
    page = Page.query.get_or_404(page_id)
    links = Link.query.filter_by(source_page_id=page.id).all()
    return render_template("page.html", page=page, links=links)

@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"
