from GHMiner import GitHubMiner
from GLMiner import GitLabMiner
import pandas as pd
import random
import glob
import json
import os

tools_repo = {
    'Aim': 'aimhubio/aim',
    'Amazon SageMaker': 'aws/sagemaker-python-sdk',
    'Azure Machine Learning': 'Azure/azure-sdk-for-python',
    'ClearML': 'allegroai/clearml',
    'Codalab': 'codalab/codalab-worksheets',
    'D6tflow': 'd6t/d6tflow',
    'DVC': 'iterative/dvc',
    'Deep Lake': 'activeloopai/deeplake',
    'Determined': 'determined-ai/determined',
    'Domino': 'dominodatalab/python-domino',
    'Guild AI': 'guildai/guildai',
    'Keepsake': 'replicate/keepsake',
    'LakeFS': 'treeverse/lakeFS',
    'MLflow': 'mlflow/mlflow',
    'ModelDB': 'VertaAI/modeldb',
    'Neptune': 'neptune-ai/neptune-client',
    'Pachyderm': 'pachyderm/pachyderm',
    'Polyaxon': 'polyaxon/polyaxon',
    'Quilt': 'quiltdata/quilt',
    'Sacred': 'IDSIA/sacred',
    'Valohai': 'valohai/valohai-cli',
    'Weights & Biases': 'wandb/wandb'
}

tools_release_date = {
    'Comet': '2017-01-01',
    'D6tflow': '2019-02-02',
    'Databricks': '2021-05-27',
    'Polyaxon': '2018-10-16',
    'SigOpt': '2014-11-01',
    'Spell': '2017-01-01',
    'Vertex AI': '2019-03-01',
    'cnvrg.io': '2020-03-31'  
}

tools_link = {
    'Comet': 'https://github.com/comet-ml',
    'Databricks': 'https://www.databricks.com/product/unity-catalog',
    'SigOpt': 'https://github.com/sigopt',
    'Spell': 'https://github.com/spellml',
    'Vertex AI': 'https://cloud.google.com/vertex-ai',
    'cnvrg.io': 'https://github.com/cnvrg'  
}

tools_keywords = {
    'Aim': 'aim',
    'Amazon SageMaker': 'sagemaker',
    'Azure Machine Learning': 'azure',
    'ClearML': 'clearml',
    'Codalab': 'codalab',
    'Comet': 'comet',
    'D6tflow': 'd6tflow',
    'DVC': 'dvc',
    'Deep Lake': 'deeplake',
    'Determined': 'determined',
    'Domino': 'domino',
    'Guild AI': 'guildai',
    'Keepsake': 'keepsake',
    'LakeFS': 'lakefs',
    'MLflow': 'mlflow',
    'ModelDB': 'modeldb',
    'Neptune': 'neptune',
    'Pachyderm': 'pachyderm',
    'Polyaxon': 'polyaxon',
    'Quilt': 'quilt',
    'Sacred': 'sacred',
    'SigOpt': 'sigopt',
    'Spell': 'spell',
    'Valohai': 'valohai',
    'Vertex AI': 'vertex',
    'Weights & Biases': 'wandb'
}

path_dataset = '../Dataset'

path_github = os.path.join(path_dataset, 'GitHub')
path_gitlab = os.path.join(path_dataset, 'GitLab')

path_github_repo = os.path.join(path_github, 'Repo')
path_gitlab_repo = os.path.join(path_gitlab, 'Repo')
path_github_repo_raw = os.path.join(path_github_repo, 'Raw')
path_gitlab_repo_raw = os.path.join(path_gitlab_repo, 'Raw')
path_github_repo_scraped = os.path.join(path_github_repo, 'Scraped')
path_gitlab_repo_scraped = os.path.join(path_gitlab_repo, 'Scraped')
path_gitlab_repo_labelled = os.path.join(path_gitlab_repo, 'labelled')

path_github_issue = os.path.join(path_github, 'Issue')
path_gitlab_issue = os.path.join(path_gitlab, 'Issue')
path_github_issue_raw = os.path.join(path_github_issue, 'Raw')
path_gitlab_issue_raw = os.path.join(path_gitlab_issue, 'Raw')

if not os.path.exists(path_github):
    os.makedirs(path_github)

if not os.path.exists(path_gitlab):
    os.makedirs(path_gitlab)

if not os.path.exists(path_github_repo):
    os.makedirs(path_github_repo)

if not os.path.exists(path_gitlab_repo):
    os.makedirs(path_gitlab_repo)

if not os.path.exists(path_github_issue):
    os.makedirs(path_github_issue)

if not os.path.exists(path_gitlab_issue):
    os.makedirs(path_gitlab_issue)

if not os.path.exists(path_github_repo_raw):
    os.makedirs(path_github_repo_raw)

if not os.path.exists(path_gitlab_repo_raw):
    os.makedirs(path_gitlab_repo_raw)

if not os.path.exists(path_github_issue_raw):
    os.makedirs(path_github_issue_raw)

if not os.path.exists(path_gitlab_issue_raw):
    os.makedirs(path_gitlab_issue_raw)

if not os.path.exists(path_github_repo_scraped):
    os.makedirs(path_github_repo_scraped)

if not os.path.exists(path_gitlab_repo_scraped):
    os.makedirs(path_gitlab_repo_scraped)

if not os.path.exists(path_gitlab_repo_labelled):
    os.makedirs(path_gitlab_repo_labelled)

github_token1 = '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'
github_token2 = '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'
github_token3 = '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'
github_token4 = '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'
github_token5 = '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'
gitlab_token1 = 'glpat-LFsxferBHR75dL9XKvos'

github_miner = GitHubMiner(github_token2)
gitlab_miner = GitLabMiner(gitlab_token1)

df = pd.read_json(os.path.join(path_dataset, 'Tools.json'))

# scrape issues of Github dependents for each tool
for index, row in df.iterrows():
    if index != 15:
        continue
    file_name = os.path.join(path_github_repo_scraped, f'{row["Name"]}.json')
    if os.path.exists(file_name):
        repos = pd.read_json(file_name)
        # filter out repos with only pr-based issues
        repos = repos[repos['#Issues'] > repos['#Pull Requests']]
        # filter out repos created before the tool's first release date
        repos = repos[repos['Repo Creation Date'] > row['First Release Date']]
        print(
            f'{row["Name"]}: {repos["#Issues"].sum() - repos["#Pull Requests"].sum()}')
        issues = github_miner.scrape_issues_list(repos['Repo'].tolist())
        if not issues.empty:
            issues.to_json(os.path.join(path_github_issue_raw,
                           f'{row["Name"]}.json'), indent=4, orient='records')
