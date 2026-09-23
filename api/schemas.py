from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):

    userId: str = Field(
        ...,
        min_length=1
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=50
    )


class RecommendationItem(BaseModel):

    itemId: str
    category: str
    price: float
    cfScore: float
    cbScore: float
    hybridScore: float


class RecommendationResponse(BaseModel):

    userId: str

    recommendations: list[
        RecommendationItem
    ]