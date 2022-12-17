from github import Github
import pandas as pd
import time


def sleep_wrapper(func, **args):
    time.sleep(3)
    return func(**args)


class GitHubMiner():
    def __init__(self, private_token):
        self.github = Github(login_or_token=private_token)

    def scrape_issues(self, repo_name):
        repo = sleep_wrapper(self.github.get_repo, full_name_or_id=repo_name)
        issues = sleep_wrapper(repo.get_issues, state='all')
        issues_data = pd.DataFrame()

        for issue in issues:
            time.sleep(3)
            if not issue.pull_request:
                reactions = issue.get_reactions()

                issue_data = {}
                issue_data['Issue_link'] = issue.html_url
                issue_data['Issue_title'] = issue.title
                issue_data['Issue_label'] = [
                    label.name for label in issue.labels]
                issue_data['Issue_creation_time'] = issue.created_at
                issue_data['Issue_closed_time'] = issue.closed_at
                issue_data['Issue_upvote_count'] = sum(
                    reaction['content'] == '+1' for reaction in reactions)
                issue_data['Issue_downvote_count'] = sum(
                    reaction['content'] == '-1' for reaction in reactions)
                issue_data['Issue_comment_count'] = issue.comments
                issue_data['Issue_body'] = issue.body

                issue_data = pd.DataFrame([issue_data])
                issues_data = pd.concat(
                    [issues_data, issue_data], ignore_index=True)

        return issues_data

    def scrape_issues_list(self, repo_list):
        issues_list_data = pd.DataFrame()

        for repo_name in repo_list:
            issues_data = self.scrape_issues(repo_name=repo_name)
            issues_list_data = pd.concat(
                [issues_list_data, issues_data], ignore_index=True)

        return issues_list_data

    def scrape_repo(self, repo_name, release_date=False):
        try:
            repo = sleep_wrapper(self.github.get_repo,
                                 full_name_or_id=repo_name)
            commits = sleep_wrapper(repo.get_commits)
            releases = sleep_wrapper(repo.get_releases)
            issues = sleep_wrapper(repo.get_issues, state='all')

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Repo Creation Date': repo.created_at,
                'Last Commit Date': commits[0].commit.author.date,
                'Topics': sleep_wrapper(repo.get_topics),
                'Language': repo.language,
                'Size': repo.size,
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Contributors': sleep_wrapper(repo.get_contributors).totalCount,
                '#Branches': sleep_wrapper(repo.get_branches).totalCount,
                '#Releases': releases.totalCount,
                '#Commits': commits.totalCount,
                '#Pull Requests': sleep_wrapper(repo.get_pulls, state='all').totalCount,
                '#Pull Requests (Open)': sleep_wrapper(repo.get_pulls, state='open').totalCount,
                '#Issues': issues.totalCount,
                '#Issues (Open)': sleep_wrapper(repo.get_issues, state='open').totalCount
            }

            if release_date and releases.totalCount > 0:
                repo_data['First Release Date'] = releases.reversed[0].created_at

            repo_data = pd.DataFrame([repo_data])
            return repo_data, pd.Dataframe()

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': err.status}
            error_data = pd.DataFrame([error_data])
            return pd.Dataframe(), error_data

    def scrape_repo_list(self, repo_list, release_date=False):
        errors_data = pd.Dataframe()
        repos_data = pd.Dataframe()

        for repo_name in repo_list:
            repo_data, error_data = self.scrape_repo(
                repo_name=repo_name, release_date=release_date)
            if not repo_data.empty:
                repos_data = pd.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                errors_data = pd.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
