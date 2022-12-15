from github import Github
import pandas as pd
import time


class GitHubMiner():
    def __init__(self, private_token):
        self.github = Github(login_or_token=private_token)

    def scrape(self, repo_name, tool_release_date=None):
        def sleep_wrapper(func, **args):
            time.sleep(3)
            return func(**args)

        try:
            repo = sleep_wrapper(self.github.get_repo,
                                 full_name_or_id=repo_name)

            commits = sleep_wrapper(repo.get_commits)
            last_commit_date = pd.to_datetime(
                commits[0].commit.author.date)
            if tool_release_date is not None and tool_release_date > last_commit_date:
                error_data = {'Repo': repo_name, 'Error': 'Unrelevant'}
                return None, error_data

            releases = sleep_wrapper(repo.get_releases)
            issues = sleep_wrapper(repo.get_issues, state='all')

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Repo Creation Date': pd.to_datetime(repo.created_at),
                'Last Commit Date': last_commit_date,
                'Topics': sleep_wrapper(repo.get_topics),
                'Language': repo.language,
                'Size': repo.size,
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Contributors': sleep_wrapper(repo.get_contributors).totalCount,
                '#Branches': sleep_wrapper(repo.get_branches).totalCount,
                '#Releases': releases.totalCount,
                '#Commits': sleep_wrapper(repo.get_commits).totalCount,
                '#Pull Requests': sleep_wrapper(repo.get_pulls, state='all').totalCount,
                '#Pull Requests (Open)': sleep_wrapper(repo.get_pulls, state='open').totalCount,
                '#Issues': issues.totalCount,
                '#Issues (Open)': sleep_wrapper(repo.get_issues, state='open').totalCount
            }

            if releases.totalCount > 0:
                repo_data['First Release Date'] = pd.to_datetime(
                    releases.reversed[0].created_at)

            return repo_data, None

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': err}
            return None, error_data

    def collect(self, repo_list, tool_release_date=None):
        errors_data = None
        repos_data = None

        for repo_name in repo_list:
            repo_data, error_data = self.scrape(
                repo_name=repo_name, tool_release_date=tool_release_date)
            if error_data is None:
                repo_data = pd.DataFrame([repo_data])
                repos_data = pd.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                error_data = pd.DataFrame([error_data])
                errors_data = pd.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
