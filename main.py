from pprint import pprint
import time

import yaml

from src.notion import NotionAPI
from src.datastore import DataStore
from src.mantis import Issue, MantisAPI


def execute():
    data_store = DataStore('./data.json')

    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        mantis = config['mantis']
        notion = config['notion']

    if mantis:
        api_token = mantis['api_token']
        base_url = mantis['base_url']
        mantisAPI = MantisAPI(base_url, api_token)
        issues = mantisAPI.get_issues_in_a_project(0)

        def is_new_aos_issue(issue: Issue) -> bool:
            # TODO reassign
            return '[AOS]' in issue.summary and issue.status == 'assigned'

        aos_issues = [issue for issue in issues if is_new_aos_issue(issue)]
        aos_issues.sort(key=lambda x: x.update_date, reverse=True)
        saved_aos_issues = data_store.get('aos_issues')
        if saved_aos_issues:
            new_aos_issues = [issue for issue in aos_issues if issue.id not in saved_aos_issues]
        else:
            new_aos_issues = aos_issues
        pprint(new_aos_issues)

    if new_aos_issues and notion:
        api_token = notion['api_token']
        database_id = notion['database_id']
        notionAPI = NotionAPI(api_token, database_id)

        def make_request(title: str, issue_id: int):
            return {
                '작업 이름': {
                    'title': [{
                        'text': {
                            'content': f'{title} (#{issue_id})',
                        },
                    }]
                },
                '태그': {
                    'multi_select': [{'name': '버그 수정'}]
                }
            }

        for issue in new_aos_issues:
            res = notionAPI.add_data(make_request(issue.summary, issue.id))
            if res:
                data_store.add('aos_issues', issue.id)
                data_store.save()
                print(f'데이터가 성공적으로 저장했습니다 ({issue.id})')

if __name__ == '__main__':
    while True:
        pprint('실행')
        execute()
        pprint('실행 완료')
        time.sleep(60)