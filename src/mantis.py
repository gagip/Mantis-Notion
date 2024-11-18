from datetime import date, datetime
import requests
from dataclasses import dataclass


@dataclass
class Project:
    id: int
    name: str

@dataclass
class Issue:
    id: int
    summary: str
    description: str
    category: str
    status: str
    update_date: datetime

def map_to_project(data: dict) -> Project:
    return Project(
        id = data['id'],
        name = data['name']
    )
    
def map_to_issue(data: dict) -> Issue:
    return Issue(
        id = data['id'],
        summary = data['summary'],
        description = data['description'],
        category= data['category']['name'],
        status = data['status']['name'],
        update_date = datetime.fromisoformat(data['updated_at'])
    )

class MantisAPI:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.headers = {
            'Authorization': api_token,
        }
        
    def call_api(self, endpoint, data = None):
        response = requests.get(f'{self.base_url}/{endpoint}', headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'API 호출 실패, HTTP 상태 코드: {response.status_code}, 내용: {response.text}')
            return None
        
    def get_all_project(self):
        res = self.call_api('api/rest/projects')
        if res:
            return [map_to_project(item) for item in res['projects']]
        else:
            return []
    
    def get_issues_in_a_project(self, project_id) -> list[Issue]:
        data = {
            'project_id': project_id,
            'page_size': 50,
            'page': 1
        }
        res = self.call_api('api/rest/issues', data = data)
        if res:
            issues = res['issues']
            return [map_to_issue(item) for item in issues]
        
        raise RuntimeError('API 호출 실패')
