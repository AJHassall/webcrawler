from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from webcrawler.ext.database import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))

class Page(db.Model, SerializerMixin):
    """
    Represents a crawled web page.
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), unique=True, nullable=False)
    title = db.Column(db.String(2048))
    content = db.Column(db.Text)
    last_crawled = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    links = relationship("Link", back_populates="source_page")

    def __repr__(self):
        return f"<Page {self.url}>"

class Link(db.Model, SerializerMixin):
    """
    Represents a link found on a crawled page.
    """
    id = db.Column(db.Integer, primary_key=True)
    source_page_id = db.Column(db.Integer, ForeignKey('page.id'), nullable=False)
    url = db.Column(db.String(2048), nullable=False)  # URL the link points to

    # Relationships
    source_page = relationship("Page", back_populates="links")

    def __repr__(self):
        return f"<Link from {self.source_page_id} to {self.url}>"