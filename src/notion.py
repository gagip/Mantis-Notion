from notion_client import Client
from typing import Dict, Any, Optional

from .logger import setup_logger

logger = setup_logger(__name__)

class NotionAPI:
    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id

    def add_data(self, properties: Dict[str, Any]):
        try:
            response = self.client.pages.create(
                parent={'database_id': self.database_id},
                properties=properties
            )
            if not response:
                raise ValueError('Notion API 응답이 비어있습니다')
            logger.info('데이터가 성공적으로 추가되었습니다.')
            return response
        except Exception as e:
            logger.error(f'오류 발생: {e}')

    def get_data(self):
        try:
            response = self.client.databases.query(
                database_id=self.database_id
            )
            return response.get('results', []) # type: ignore
        except Exception as e:
            logger.error(f'오류 발생: {e}')
            return []
