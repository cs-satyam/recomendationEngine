from fastapi import APIRouter, HTTPException

from api.schemas import (
    RecommendationRequest,
    RecommendationResponse
)

from app.recommender import RecommendationEngine


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


# Load model once when API starts
engine = RecommendationEngine()


@router.post(
    "",
    response_model=RecommendationResponse
)
def get_recommendations(
    request: RecommendationRequest
):

    try:

        recommendations = (
            engine.get_recommendations(
                user_id=request.userId,
                limit=request.limit
            )
        )

        return {
            "userId": request.userId,
            "recommendations": recommendations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )