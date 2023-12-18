import pytest

from src.wb_looker.models import Card, Feedback
from tests.conftest import (EXAMPLE_CARD_ID, EXAMPLE_CARD_RESPONSE,
                            EXAMPLE_EMPTY_FEEDBACK_RESPONSE,
                            EXAMPLE_FEEDBACK_RESPONSE, EXAMPLE_NAME,
                            EXAMPLE_PARAMS, EXAMPLE_RATING,
                            EXAMPLE_REVIEW_RATING, EXAMPLE_ROOT_ID)


def test_card_model():
    card = Card.from_resp(EXAMPLE_CARD_RESPONSE)
    assert card.state == 0
    assert card.params == EXAMPLE_PARAMS
    products = card.data.products
    assert len(products) == 1
    assert products[0].id == EXAMPLE_CARD_ID
    assert products[0].root == EXAMPLE_ROOT_ID
    assert products[0].name == EXAMPLE_NAME
    assert products[0].rating == EXAMPLE_RATING
    assert products[0].review_rating == EXAMPLE_REVIEW_RATING


@pytest.mark.parametrize(
    "response, is_empty",
    [
        (EXAMPLE_EMPTY_FEEDBACK_RESPONSE, True),
        (EXAMPLE_FEEDBACK_RESPONSE, False)
    ]
)
def test_feedback_is_empty(response, is_empty):
    feedback = Feedback.from_resp(response)
    assert feedback.is_empty == is_empty


def test_feedback_get_comments():
    feedback = Feedback.from_resp(EXAMPLE_FEEDBACK_RESPONSE)
    comments = feedback.get_comments
    assert len(comments) == 8
