from typing import Optional

from pydantic import BaseModel


class RecommendationItem(BaseModel):
    article_id: str

    product_name: Optional[str] = None
    product_type: Optional[str] = None
    product_group: Optional[str] = None
    colour: Optional[str] = None
    department: Optional[str] = None
    section: Optional[str] = None
    description: Optional[str] = None

    score: float
    collaborative_score: Optional[float] = None
    content_score: Optional[float] = None
    reason: Optional[str] = None


class RecommendationResponse(BaseModel):
    customer_id: str
    count: int
    recommendations: list[RecommendationItem]