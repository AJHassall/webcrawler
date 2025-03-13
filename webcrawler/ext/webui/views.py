from flask import abort, render_template
from flask_simplelogin import login_required

from webcrawler.models import Product


def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"
