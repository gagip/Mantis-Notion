from pprint import pformat
import time

import yaml

from src.notion import NotionAPI, post_bug_report
from src.datastore import DataStore
from src.mantis import Issue, MantisAPI
from src.logger import setup_logger

logger = setup_logger(__name__)


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
            return all([
                '[AOS]' in issue.summary, 
                issue.status == 'assigned', 
                issue.id not in data_store.get('aos_issues')
            ])

        aos_issues = [issue for issue in issues if is_new_aos_issue(issue)]
        aos_issues.sort(key=lambda x: x.update_date, reverse=True)
        saved_aos_issues = data_store.get('aos_issues')
        if saved_aos_issues:
            new_aos_issues = [issue for issue in aos_issues if issue.id not in saved_aos_issues]
        else:
            new_aos_issues = aos_issues
        logger.debug(pformat(new_aos_issues))

    if new_aos_issues and notion:
        api_token = notion['api_token']
        database_id = notion['database_id']
        notionAPI = NotionAPI(api_token, database_id)

        for issue in new_aos_issues:            
            res = post_bug_report(notionAPI, issue)
            assert res
            
            logger.debug(res)
            data_store.add('aos_issues', issue.id)
            data_store.save()
            logger.debug(f'데이터가 성공적으로 저장했습니다 ({issue.id})')

if __name__ == '__main__':
    while True:
        logger.info('실행')
        execute()
        logger.info('실행 완료')
        time.sleep(300)
        # TODO 구글 플레이스토어 배포 성공 -> 노션 페이지 출시됨으로 변경