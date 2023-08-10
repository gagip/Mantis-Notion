import yaml
from src.mantis.mantis import MantisAPI

if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        mantis = config['mantis']

    if mantis:
        api_token = mantis['api_token']
        base_url = mantis['base_url']
        product_names = mantis['projects']
        mantisAPI = MantisAPI(base_url, api_token)
        projects = [project
                    for project in mantisAPI.get_all_project()
                    if project.name in product_names]
        project_ids = list(map(lambda x : x.id, projects))
        print(project_ids)
