import requests
from .models import (Project, Issue)

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
            return [Project(**item) for item in res['projects']]
        else:
            return []
    
    def get_issues_in_a_project(self, project_id):
        data = {
            "project_id": project_id,
            "page_size": 10,
            "page": 1
        }
        res = self.call_api('api/rest/issues', data = data)
        if res:
            res['status'] = res['status']['label']
            return Issue(**res)
        return res
