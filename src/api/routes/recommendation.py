from fastapi import APIRouter, HTTPException, Query

from src.recommendation.recommendation_service import (
    RecommendationService,
)

from src.schemas.recommendation_schema import RecommendationResponse

router = APIRouter()


@router.get(
    "/{customer_id}",
    response_model=RecommendationResponse,
)
async def get_recommendations(
    customer_id: str,
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):
    try:
        if not RecommendationService.has_customer(
            customer_id
        ):
            raise HTTPException(
                status_code=404,
                detail=(
                    f"No recommendations found for "
                    f"customer '{customer_id}'."
                ),
            )

        recommendations = (
            RecommendationService.get_recommendations(
                customer_id=customer_id,
                limit=limit,
            )
        )

        return RecommendationResponse(
            customer_id=customer_id,
            count=len(recommendations),
            recommendations=recommendations,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate recommendations: "
                f"{str(exc)}"
            ),
        )