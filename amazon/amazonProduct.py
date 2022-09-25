import persistent


class AmazonProduct(persistent.Persistent):
    def __init__(self, product_name, overall_rating, num_reviews, review_list):
        super().__init__()
        self.product_name = product_name
        self.overall_rating = overall_rating
        self.num_reviews = num_reviews
        self.review_list = review_list

    
    def add_review(self, review):
        self.review_list.append(review)
        self._p_changed = True
