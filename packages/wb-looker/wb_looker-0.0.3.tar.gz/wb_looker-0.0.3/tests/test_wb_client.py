from multiprocessing import Queue

import pytest
from pytest_httpx import HTTPXMock

from src.wb_looker.client import WB
from src.wb_looker.const import WB_CARD_URL, WB_FEEDBACK_URLS
from tests.conftest import (EXAMPLE_CARD_ID, EXAMPLE_CARD_RESPONSE,
                            EXAMPLE_EMPTY_FEEDBACK_RESPONSE,
                            EXAMPLE_FEEDBACK_RESPONSE, EXAMPLE_FEEDBACKS,
                            EXAMPLE_NAME, EXAMPLE_PARAMS, EXAMPLE_RATING,
                            EXAMPLE_REVIEW_RATING, EXAMPLE_ROOT_ID)


@pytest.mark.asyncio
async def test_wb_parser_get_card(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{WB_CARD_URL}{EXAMPLE_CARD_ID}",
        json=EXAMPLE_CARD_RESPONSE
    )

    q = Queue()
    q.put(EXAMPLE_CARD_ID)

    wb = WB()
    card = await wb.get_card(EXAMPLE_CARD_ID)
    assert card.state == 0
    assert card.params == EXAMPLE_PARAMS
    assert len(card.data.products) == 1
    product = card.data.products[0]
    assert product.id == EXAMPLE_CARD_ID
    assert product.root == EXAMPLE_ROOT_ID
    assert product.name == EXAMPLE_NAME
    assert product.rating == EXAMPLE_RATING
    assert product.review_rating == EXAMPLE_REVIEW_RATING


@pytest.mark.asyncio
async def test_wb_parser_get_product_feedbacks(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{WB_CARD_URL}{EXAMPLE_CARD_ID}",
        json=EXAMPLE_CARD_RESPONSE
    )
    httpx_mock.add_response(
        url=f'{WB_FEEDBACK_URLS[0]}{EXAMPLE_ROOT_ID}',
        json=EXAMPLE_FEEDBACK_RESPONSE
    )

    q = Queue()
    q.put(EXAMPLE_CARD_ID)

    wb = WB()
    card = await wb.get_card(EXAMPLE_CARD_ID)
    feedbacks = await wb.get_feedbacks_for_card(card)

    assert len(feedbacks) == 1
    assert EXAMPLE_ROOT_ID in feedbacks
    assert len(feedbacks[EXAMPLE_ROOT_ID]) == len(EXAMPLE_FEEDBACKS)
    for i, feedback in enumerate(feedbacks[EXAMPLE_ROOT_ID]):
        assert feedback == EXAMPLE_FEEDBACKS[i].lower()


@pytest.mark.asyncio
async def test_wb_parser_get_product_feedbacks_empty(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{WB_CARD_URL}{EXAMPLE_CARD_ID}",
        json=EXAMPLE_CARD_RESPONSE
    )
    httpx_mock.add_response(
        url=f'{WB_FEEDBACK_URLS[0]}{EXAMPLE_ROOT_ID}',
        json=EXAMPLE_EMPTY_FEEDBACK_RESPONSE
    )
    httpx_mock.add_response(
        url=f'{WB_FEEDBACK_URLS[1]}{EXAMPLE_ROOT_ID}',
        json=EXAMPLE_EMPTY_FEEDBACK_RESPONSE
    )

    q = Queue()
    q.put(EXAMPLE_CARD_ID)

    wb = WB()
    card = await wb.get_card(EXAMPLE_CARD_ID)
    feedbacks = await wb.get_feedbacks_for_card(card)
    assert feedbacks == {EXAMPLE_ROOT_ID: []}
