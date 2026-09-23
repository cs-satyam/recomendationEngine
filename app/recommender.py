import os
import joblib
import pandas as pd
import numpy as np


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODELS_DIR = os.path.join(BASE_DIR, "models")


class RecommendationEngine:

    def __init__(self):
        print("Loading recommendation models...")

        # Collaborative Filtering
        self.cf_model = joblib.load(
            os.path.join(
                MODELS_DIR,
                "cf_model.pkl"
            )
        )

        # Content-Based preprocessing
        self.cb_preprocessor = joblib.load(
            os.path.join(
                MODELS_DIR,
                "cb_preprocessor.pkl"
            )
        )

        # Content-Based similarity matrix
        self.similarity_matrix = joblib.load(
            os.path.join(
                MODELS_DIR,
                "cb_similarity_matrix.pkl"
            )
        )

        # Product information
        self.products = pd.read_csv(
            os.path.join(
                MODELS_DIR,
                "cb_products.csv"
            )
        )

        self.products["Item_ID"] = (
            self.products["Item_ID"].astype(str)
        )

        # Item -> similarity matrix index
        self.item_to_index = {
            item_id: index
            for index, item_id
            in enumerate(self.products["Item_ID"])
        }

        print("All models loaded successfully.")

    # --------------------------------------------------
    # CF
    # --------------------------------------------------

    def predict_rating(self, user_id, item_id):

        prediction = self.cf_model.predict(
            user_id,
            item_id
        )

        return float(prediction.est)

    # --------------------------------------------------
    # CB
    # --------------------------------------------------

    def get_similar_items(
        self,
        item_id,
        limit=10
    ):

        if item_id not in self.item_to_index:
            return []

        index = self.item_to_index[item_id]

        similarities = self.similarity_matrix[index]

        indices = np.argsort(
            similarities
        )[::-1]

        results = []

        for i in indices:

            if i == index:
                continue

            product = self.products.iloc[i]

            results.append({
                "itemId": str(product["Item_ID"]),
                "category": str(product["Category"]),
                "price": float(product["Price"]),
                "similarity": float(
                    similarities[i]
                )
            })

            if len(results) >= limit:
                break

        return results

    # --------------------------------------------------
    # CF recommendations
    # --------------------------------------------------

    def get_cf_recommendations(
        self,
        user_id,
        limit=10
    ):

        results = []

        for item_id in self.products["Item_ID"]:

            try:

                score = self.predict_rating(
                    user_id,
                    item_id
                )

                results.append({
                    "itemId": item_id,
                    "cfScore": score
                })

            except Exception:
                continue

        results.sort(
            key=lambda x: x["cfScore"],
            reverse=True
        )

        return results[:limit]

    # --------------------------------------------------
    # HYBRID
    # --------------------------------------------------

    def get_recommendations(
        self,
        user_id,
        limit=10
    ):

        candidates = []

        # Generate CF scores for every product
        for item_id in self.products["Item_ID"]:

            try:

                cf_score = self.predict_rating(
                    user_id,
                    item_id
                )

                candidates.append({
                    "itemId": item_id,
                    "cfScore": cf_score
                })

            except Exception:
                continue

        if not candidates:
            return []

        # Normalize CF scores
        scores = [
            item["cfScore"]
            for item in candidates
        ]

        min_score = min(scores)
        max_score = max(scores)

        for item in candidates:

            if max_score == min_score:
                item["cfNormalized"] = 0.5

            else:
                item["cfNormalized"] = (
                    item["cfScore"] - min_score
                ) / (
                    max_score - min_score
                )

        # Add product information
        product_lookup = self.products.set_index(
            "Item_ID"
        )

        for item in candidates:

            product = product_lookup.loc[
                item["itemId"]
            ]

            item["category"] = str(
                product["Category"]
            )

            item["price"] = float(
                product["Price"]
            )

            # Default CB score
            item["cbScore"] = 0.0

        # ------------------------------------------------
        # Content preference
        #
        # For now use the user's strongest categories
        # later from interaction history/database.
        # ------------------------------------------------

        # Simple category score based on CF candidates.
        #
        # This will be replaced by actual user-history
        # category preferences once Spring Boot/database
        # integration is added.

        category_counts = {}

        for item in candidates:

            category = item["category"]

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        max_category_count = max(
            category_counts.values()
        )

        for item in candidates:

            item["cbScore"] = (
                category_counts[
                    item["category"]
                ] / max_category_count
            )

            # Hybrid weighting
            item["hybridScore"] = (
                0.7 * item["cfNormalized"]
                +
                0.3 * item["cbScore"]
            )

        # Sort
        candidates.sort(
            key=lambda x: x["hybridScore"],
            reverse=True
        )

        # Return clean response
        recommendations = []

        for item in candidates[:limit]:

            recommendations.append({
                "itemId": item["itemId"],
                "category": item["category"],
                "price": item["price"],
                "cfScore": round(
                    item["cfScore"], 4
                ),
                "cbScore": round(
                    item["cbScore"], 4
                ),
                "hybridScore": round(
                    item["hybridScore"], 4
                )
            })

        return recommendations