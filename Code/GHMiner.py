from github import Github
import pandas
import random
import time


class GithubMiner():
    def __init__(self, token):
        self.github = Github(token)
        self.repo_columns = [
            'Repo',
            'Link',
            'Archived',
            'Creation Date',
            'Topics',
            '#Star',
            '#Watch',
            '#Fork',
            '#Releases',
            '#Contributors',
            'Language',
            'Size',
            '#Open Issues',
            '#Pull Requests',
            '#Branches',
            '#Tags',
            '#Commits',
            '#Comments',
            '#Downloads',
            '#Deployments'
        ]
        self.error_columns = [
            'Repo',
            'Error'
        ]

    def scrape(self, repo_name, name=None, date=None, real_creation_date=True):
        def sleep_wrapper(func, **args):
            time.sleep(random.random() + 0.5)
            return func(**args)

        try:
            repo = sleep_wrapper(self.github.get_repo,
                                 full_name_or_id=repo_name)

            creation_date = repo.created_at
            if not real_creation_date:
                creation_date = sleep_wrapper(
                    repo.get_commits).reversed[0].commit.author.date

            if date is not None:
                last_commit_date = sleep_wrapper(
                    repo.get_commits)[0].commit.author.date
                if date > last_commit_date:
                    error_data = {'Repo': repo_name, 'Error': 'Unrelated'}
                    return None, error_data

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Archived': repo.archived,
                'Creation Date': creation_date,
                'Topics': sleep_wrapper(repo.get_topics),
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Releases': sleep_wrapper(repo.get_releases).totalCount,
                '#Contributors': sleep_wrapper(repo.get_contributors).totalCount,
                'Language': repo.language,
                'Size': repo.size,
                '#Open Issues': repo.open_issues_count,
                '#Pull Requests': sleep_wrapper(repo.get_pulls).totalCount,
                '#Branches': sleep_wrapper(repo.get_branches).totalCount,
                '#Tags': sleep_wrapper(repo.get_tags).totalCount,
                '#Commits': sleep_wrapper(repo.get_commits).totalCount,
                '#Comments': sleep_wrapper(repo.get_comments).totalCount,
                '#Downloads': sleep_wrapper(repo.get_downloads).totalCount,
                '#Deployments': sleep_wrapper(repo.get_deployments).totalCount,
            }

            if name is not None:
                repo_data['Name'] = name

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': str(err)}
            return None, error_data

        return repo_data, None

    def collect(self, repo_names, name=None, date=None, real_creation_date=True):
        repos_data = pandas.DataFrame(columns=self.repo_columns)
        errors_data = pandas.DataFrame(columns=self.error_columns)

        for repo_name in repo_names:
            repo_data, error_data = self.scrape(
                repo_name=repo_name, name=name, date=date, real_creation_date=real_creation_date)

            if error_data is None:
                repo_data = pandas.DataFrame([repo_data])
                repos_data = pandas.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                error_data = pandas.DataFrame([error_data])
                errors_data = pandas.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
