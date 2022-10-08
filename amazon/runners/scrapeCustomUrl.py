from amazon.AmazonScrape import add_product


if __name__ == "__main__":
    db = add_product()
    with db.transaction() as conn:
        product = conn.root.products[0]
        print(f"Product Name: {product.product_name}")
        print(f"Stars (out of 5): {product.overall_rating}")
        print(f"Number of Ratings: {product.num_reviews}")
