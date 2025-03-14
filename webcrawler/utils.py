import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from webcrawler.models import Page, Link  # Import your Page and Link models
from webcrawler.ext.database import db  # Import your database session

MAX_REQUESTS = 10
REQUEST_DELAY = 0.3  # Seconds

crawled_urls = set()  # Keep track of crawled URLs to avoid duplicates
total_requests = 0

def scrape_page(url, base_url=None):
    """
    Recursively scrapes data from a web page, including links.

    Args:
        url (str): The URL of the page to scrape.
        base_url (str, optional): The base URL for resolving relative links.
                                 Defaults to None (uses the initial URL).

    Returns:
        dict: A dictionary containing the extracted data, or None if scraping fails
    """
    global total_requests

    if total_requests >= MAX_REQUESTS:
        print("Max requests reached. Stopping.")
        return None

    if url in crawled_urls:
        print(f"Already crawled: {url}")
        return None

    try:
        total_requests += 1
        print(f"Crawling: {url} (Request {total_requests})")

        time.sleep(REQUEST_DELAY)  # Rate limiting

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        crawled_urls.add(url)  # Add URL to crawled URLs

        data = {}
        data["url"] = url

        title = soup.title.text if soup.title else None
        data["title"] = title

        # --- Extract Content (HTML) ---
        data["content"] = str(soup)  # Store the entire HTML content

        metadata = {}
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag:
            metadata["description"] = description_tag.get("content")

        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        if keywords_tag:
            metadata["keywords"] = keywords_tag.get("content")

        data["metadata"] = metadata

        # --- Save Page to DB ---
        page = Page(url=data["url"], title=data["title"], content=data["content"])
        db.session.add(page)
        db.session.commit()

        # --- Extract Links and Recursively Crawl ---
        # Initialize links as a list here
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            text = link.text.strip()
            if href:
                absolute_url = urljoin(url, href)  # Use current URL as base
                parsed_url = urlparse(absolute_url)
                if parsed_url.scheme in ("http", "https"):  # Only crawl http/https
                    links.append({"url": absolute_url, "text": text})

                    # --- Recursive Call ---
                    scrape_page(absolute_url, url)  # Recursive call

                    # --- Save Link to DB ---
                    link_obj = Link(source_page_id=page.id, url=absolute_url)
                    db.session.add(link_obj)
                    db.session.commit()

        data["links"] = links
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {url}: {e}")
        db.session.rollback()  # Rollback changes on any exception
        return None