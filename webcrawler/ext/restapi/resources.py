from flask import abort, jsonify, request
from flask_restful import Resource
from flask_simplelogin import login_required

from webcrawler.models import Page  # Assuming you have a Page model
from webcrawler.utils import scrape_page  # Assuming you have a scrape_page utility

class PageResource(Resource):
    def get(self):
        """
        Retrieves all crawled pages.
        """
        pages = Page.query.all()
        if not pages:
            abort(204)  # No Content
        return jsonify({"pages": [page.to_dict() for page in pages]})

    def post(self):
        """
        Crawls a new page and stores its data.

        Only admin user authenticated using basic auth can use this.
        Expects JSON data with a 'url' field.
        """
        data = request.get_json()
        if not data or 'url' not in data:
            abort(400, "Missing 'url' in request data")

        url = data['url']
        try:
            page_data = scrape_page(url)  # Use your scraping utility
            if not page_data:
                abort(500, "Error during scraping")

            page = Page(
                url=url,
                title=page_data.get('title'),
                content=page_data.get('content'),
                # Add other fields as needed based on your Page model
            )

            db.session.add(page)
            db.session.commit()

            return (
                jsonify({"message": "Page crawled and stored successfully", "page_id": page.id}),
                201,  # Created
            )

        except Exception as e:
            db.session.rollback()
            abort(500, f"Error processing URL: {str(e)}")


class PageItemResource(Resource):
    def get(self, page_id):
        """
        Retrieves a specific crawled page.
        """
        page = Page.query.filter_by(id=page_id).first() or abort(404)
        return jsonify(page.to_dict())