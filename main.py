from pprint import pprint

import yaml

from src.datastore import DataStore
from src.mantis import Issue, MantisAPI

if __name__ == '__main__':
    data_store = DataStore('./data.json')

    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        mantis = config['mantis']
        notion = config['notion']

    if mantis:
        api_token = mantis['api_token']
        base_url = mantis['base_url']
        product_names = mantis['projects']
        mantisAPI = MantisAPI(base_url, api_token)
        projects = [project for project in mantisAPI.get_all_project()
                    if project.name in product_names]
        (mobile_project_id, watch_project_id) = [
            project.id for project in projects
        ]

        issues = mantisAPI.get_issues_in_a_project(0)

        def is_new_aos_issue(issue: Issue) -> bool:
            return '[AOS]' in issue.summary and issue.status == 'new'

        aos_issues = [issue for issue in issues if is_new_aos_issue(issue)]
        aos_issues.sort(key=lambda x: x.update_date, reverse=True)
        pprint(aos_issues)

    if notion:
        pass
