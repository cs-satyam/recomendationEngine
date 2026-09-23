from recommender import RecommendationEngine


def main():

    engine = RecommendationEngine()

    user_id = "User_913"

    print()
    print("=" * 60)
    print("HYBRID RECOMMENDATION TEST")
    print("=" * 60)

    recommendations = engine.get_recommendations(
        user_id=user_id,
        limit=10
    )

    print(f"User: {user_id}")
    print(
        f"Recommendations: {len(recommendations)}"
    )

    print()

    for index, item in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{index}. "
            f"{item['itemId']} | "
            f"{item['category']} | "
            f"₹{item['price']:.2f} | "
            f"CF={item['cfScore']:.4f} | "
            f"CB={item['cbScore']:.4f} | "
            f"Hybrid={item['hybridScore']:.4f}"
        )


if __name__ == "__main__":
    main()