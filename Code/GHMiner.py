from github import Github
import pandas as pd
import time


class GitHubMiner():
    def __init__(self, private_token):
        self.github = Github(login_or_token=private_token)
        self.repo_columns = [
            'Repo',
            'Link',
            'Archived',
            'Creation Date',
            'First Activity Date',
            'Last Activity Date',
            'Topics',
            '#Star',
            '#Watch',
            '#Fork',
            '#Releases',
            '#Contributors',
            'Language',
            'Size',
            '#Issues',
            '#Pull Requests',
            '#Branches',
            '#Commits',
            '#Comments',
            '#Deployments'
        ]
        self.error_columns = [
            'Repo',
            'Error'
        ]

    def scrape(self, repo_name, name=None, date=None):
        def sleep_wrapper(func, **args):
            time.sleep(0.5)
            return func(**args)

        try:
            repo = sleep_wrapper(self.github.get_repo,
                                 full_name_or_id=repo_name)

            commits = sleep_wrapper(repo.get_commits)
            last_commit_date = pd.to_datetime(commits[0].commit.author.date).to_datetime64()
            if date is not None and date > last_commit_date:
                error_data = {'Repo': repo_name, 'Error': 'Unrelevant'}
                return None, error_data

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Archived': repo.archived,
                'Creation Date': pd.to_datetime(repo.created_at).to_datetime64(),
                'First Activity Date': pd.to_datetime(commits.reversed[0].commit.author.date).to_datetime64(),
                'Last Activity Date': last_commit_date,
                'Topics': sleep_wrapper(repo.get_topics),
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Releases': sleep_wrapper(repo.get_releases).totalCount,
                '#Contributors': sleep_wrapper(repo.get_contributors).totalCount,
                'Language': repo.language,
                'Size': repo.size,
                '#Issues': sleep_wrapper(repo.get_issues, state='all').totalCount,
                '#Pull Requests': sleep_wrapper(repo.get_pulls, state='all').totalCount,
                '#Branches': sleep_wrapper(repo.get_branches).totalCount,
                '#Commits': sleep_wrapper(repo.get_commits).totalCount,
                '#Comments': sleep_wrapper(repo.get_comments).totalCount,
                '#Deployments': sleep_wrapper(repo.get_deployments).totalCount
            }

            if name is not None:
                repo_data['Name'] = name

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': str(err)}
            return None, error_data

        return repo_data, None

    def collect(self, repo_names, name=None, date=None):
        repos_data = pd.DataFrame(columns=self.repo_columns)
        errors_data = pd.DataFrame(columns=self.error_columns)

        for repo_name in repo_names:
            repo_data, error_data = self.scrape(
                repo_name=repo_name, name=name, date=date)

            if error_data is None:
                repo_data = pd.DataFrame([repo_data])
                repos_data = pd.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                error_data = pd.DataFrame([error_data])
                errors_data = pd.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
