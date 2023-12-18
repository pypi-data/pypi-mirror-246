from typing import List

from httpx import AsyncClient

from .const import WB_CARD_URL, WB_FEEDBACK_URLS
from .models import Card, Feedback


class WB:
    def __init__(self):
        self.client = AsyncClient()

    async def get_card(self, nm_id: int) -> Card:
        response = await self.client.get(url=f"{WB_CARD_URL}{nm_id}")
        return Card.from_resp(response.json())

    async def get_feedbacks_for_card(self, card: Card) -> dict:
        feedbacks = {}
        for item in card.data.products:
            feedbacks[item.root] = await self.get_product_feedbacks(item.root)
        return feedbacks

    async def get_product_feedbacks(self, root_id: int) -> List[str]:
        for url in WB_FEEDBACK_URLS:
            response = await self.client.get(url=f"{url}{root_id}")
            feedback = Feedback.from_resp(response.json())
            if feedback.is_empty:
                continue

            return feedback.get_comments
        return []
