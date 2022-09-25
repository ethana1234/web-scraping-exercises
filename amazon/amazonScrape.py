from base.scrape import Scraper
from .amazonProduct import AmazonProduct


class AmazonReviewScraper(Scraper):
    def __init__(self):
        super().__init__()
        with self.db.transaction() as conn:
            # Add products list to db if it doesn't exist
            if not hasattr(conn.root, "products"):
                conn.root.products = []

    def add_product(self, URL=None):
        self.get_html_data(URL)
        product_name = self.webpage_soup.find("span", id="productTitle").get_text(strip=True)
        overall_review_info = self.webpage_soup.find("div", id="averageCustomerReviews")
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
        review_list_soup = self.webpage_soup.find_all("div", class_="a-section review aok-relative")
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
        with self.db.transaction() as conn:
            product = AmazonProduct(product_name, overall_rating, num_reviews, review_list)
            conn.root.products.append(product)

