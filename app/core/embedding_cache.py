class EmbeddingCache:

    def __init__(self):

        # Product Search
        self.product_ids = []
        self.products = {}
        self.product_matrix = None

        # Knowledge Bases
        self.kb_vectors = {
            "/chat": [],
            "/recommendation": [],
            "/color": [],
            "/outfit": []
        }

cache = EmbeddingCache()