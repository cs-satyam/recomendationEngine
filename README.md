# Ecommerce Recommendation ML Service

A FastAPI service that returns hybrid product recommendations by combining collaborative-filtering (CF) estimates with a content-based (CB) category score.

## What it does

- Loads the trained CF model, content preprocessor, similarity matrix, and product catalogue from `models/` when the API starts.
- Scores every product for a supplied user ID.
- Normalizes the CF scores and combines them with a category-based CB score using a `70% CF / 30% CB` weighting.
- Returns the highest-ranked products with their category, price, and component scores.

## Project layout

```text
api/                 FastAPI application, route, and request/response schemas
app/                 Recommendation engine and local test script
models/              Serialized models and product catalogue required at runtime
requirements.txt     Python dependencies
```

## Model-development notebook

The recommendation models and supporting artifacts were developed in the [Recommendation Engine Kaggle notebook](https://www.kaggle.com/code/satyam5641/recomendation-engine).

## Requirements

- Python 3.10 or later recommended
- The files in `models/` must remain available:
  - `cf_model.pkl`
  - `cb_preprocessor.pkl`
  - `cb_similarity_matrix.pkl`
  - `cb_products.csv`

## Setup and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.main:app --reload
```

The service starts at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service status |
| `GET` | `/health` | Health check |
| `POST` | `/api/recommendations` | Hybrid recommendations for a user |

### Request example

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/recommendations" `
  -ContentType "application/json" `
  -Body '{"userId":"User_913","limit":10}'
```

`userId` is required. `limit` defaults to `10` and accepts values from `1` through `50`.

### Response example

```json
{
  "userId": "User_913",
  "recommendations": [
    {
      "itemId": "Item_42",
      "category": "Sports",
      "price": 241.23,
      "cfScore": 4.125,
      "cbScore": 1.0,
      "hybridScore": 0.9125
    }
  ]
}
```

## Notes

The current CB contribution is based on category frequency among recommendation candidates. The similarity matrix is loaded and is available through `RecommendationEngine.get_similar_items()`, while personalized interaction-history-based content preferences are intended for a future database/Spring Boot integration.
