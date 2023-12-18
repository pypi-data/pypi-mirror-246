from typing import Any, List, Optional

from pydantic import BaseModel, Field


class FeedbackItem(BaseModel):
    id: str
    nm_id: int = Field(..., alias='nmId')
    text: str
    product_valuation: int = Field(..., alias='productValuation')


class Feedback(BaseModel):
    count: int = Field(..., alias='feedbackCount')
    count_with_photo: int = Field(..., alias='feedbackCountWithPhoto')
    count_with_text: int = Field(..., alias='feedbackCountWithText')
    items: Optional[List[FeedbackItem]] = Field(..., alias='feedbacks')

    @classmethod
    def from_resp(cls, response: dict) -> 'Feedback':
        return cls(**response)

    @property
    def is_empty(self) -> bool:
        return not bool(self.items)

    @property
    def get_comments(self) -> List[str]:
        return [item.text.lower() for item in self.items]


class ProductItem(BaseModel):
    id: int
    root: int
    name: str
    rating: float
    review_rating: float = Field(..., alias='reviewRating')


class Products(BaseModel):
    products: List[ProductItem]


class Card(BaseModel):
    state: int
    params: Any
    data: Products

    @classmethod
    def from_resp(cls, response: dict) -> 'Card':
        return cls(**response)
