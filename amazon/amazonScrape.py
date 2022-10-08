from ZODB import DB
from base.Scrape import get_html_data
from .AmazonProduct import AmazonProduct

def add_product(db=None, URL=None):
    db = DB(db) # DB is in memory if None

    webpage_soup = get_html_data(URL)
    product_name = webpage_soup.find("span", id="productTitle").get_text(strip=True)
    overall_review_info = webpage_soup.find("div", id="averageCustomerReviews")
    overall_rating = float(
        overall_review_info
        .find("span", id="acrPopover")
        .find("span", class_="a-icon-alt")
        .get_text(strip=True)
        .split(" ")[0]
    )
    num_reviews = int(
        overall_review_info
        .find("span", id="acrCustomerReviewText")
        .get_text(strip=True)
        .replace(",", "")
        .split(' ')[0]
    )
    review_list_soup = webpage_soup.find_all("div", class_="a-section review aok-relative")
    review_list = []
    for review in review_list_soup:
        rating = float(
            review
            .find("i", attrs={"data-hook": "review-star-rating"})
            .get_text(strip=True)
            .split(" ")[0]
        )
        title = (
            review
            .find("a", attrs={"data-hook": "review-title"})
            .get_text(strip=True)
        )
        body = (
            review
            .find("div", attrs={"data-hook": "review-collapsed"})
            .get_text(strip=True)
        )
        review_entry = {
            "rating": rating,
            "title": title,
            "body": body
        }
        review_list.append(review_entry)
        
    # Add to db
    with db.transaction() as conn:
        # Add products list to db if it doesn't exist
        if not hasattr(conn.root, "products"):
            conn.root.products = []
        product = AmazonProduct(product_name, overall_rating, num_reviews, review_list)
        conn.root.products.append(product)

    return db

