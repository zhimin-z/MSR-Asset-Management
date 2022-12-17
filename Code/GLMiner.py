from gitlab import Gitlab
import pandas as pd
import operator
import time


def sleep_wrapper(func, **args):
    time.sleep(0.1)
    return func(**args)


class GitLabMiner():
    def __init__(self, private_token):
        self.gitlab = Gitlab(private_token=private_token)

    def scrape_issues(self, repo_name):
        repo = sleep_wrapper(self.gitlab.projects.get, repo_name)
        issues = sleep_wrapper(repo.issues.list, get_all=True, state='all')

        issues_data = None
        for issue in issues:
            issue_data = {}
            issue_data['Issue_link'] = issue.web_url
            issue_data['Issue_title'] = issue.title
            issue_data['Issue_state'] = issue.state
            issue_data['Issue_label'] = issue.labels
            issue_data['Issue_creation_time'] = issue.created_at
            issue_data['Issue_closed_time'] = issue.closed_at
            issue_data['Issue_upvote_count'] = issue.upvotes
            issue_data['Issue_downvote_count'] = issue.downvotes
            issue_data['Issue_body'] = issue.description
            issue_data = pd.DataFrame(issue_data)
            issues_data = pd.concat(
                [issues_data, issue_data], ignore_index=True)
            time.sleep(0.1)

        return issues_data

    def scrape_issues_list(self, repo_list):
        issues_list_data = None

        for repo_name in repo_list:
            issues_data = self.scrape_issues(repo_name=repo_name)
            issues_list_data = pd.concat(
                [issues_list_data, issues_data], ignore_index=True)

        return issues_list_data

    def scrape_repo(self, repo_name, release_date=False):
        try:
            repo = sleep_wrapper(self.gitlab.projects.get, repo_name)
            commits = sleep_wrapper(repo.commits.list, get_all=True)
            releases = sleep_wrapper(repo.releases.list, get_all=True)
            issues = sleep_wrapper(repo.issues.list, get_all=True, state='all')

            repo_data = {
                'Repo': repo_name,
                'Link': repo.http_url_to_repo,
                'Repo Creation Date': pd.to_datetime(repo.created_at),
                'Last Commit Date': pd.to_datetime(commits[0].created_at),
                'Topics': repo.topics,
                'Language': max(sleep_wrapper(repo.languages).items(), key=operator.itemgetter(1))[0],
                '#Star': repo.star_count,
                '#Fork': repo.forks_count,
                '#Member': len(sleep_wrapper(repo.members.list, get_all=True)),
                '#Branches': len(sleep_wrapper(repo.branches.list, get_all=True)),
                '#Releases': len(releases),
                '#Commits': len(commits),
                '#Issues': len(issues),
                '#Issues (Open)': len(sleep_wrapper(repo.issues.list, get_all=True, state='opened'))
            }

            try:
                repo_data['#Merge Requests'] = len(sleep_wrapper(
                    repo.mergerequests.list, get_all=True, state='all'))
                repo_data['#Merge Requests (Open)'] = len(sleep_wrapper(
                    repo.mergerequests.list, get_all=True, state='opened'))
            except:
                repo_data['#Merge Requests'] = 0
                repo_data['#Merge Requests (Open)'] = 0

            if release_date and len(releases) > 0:
                repo_data['First Release Date'] = pd.to_datetime(
                    releases[-1].created_at)

            repo_data = pd.DataFrame([repo_data])
            return repo_data, None

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': err.status}
            error_data = pd.DataFrame([error_data])
            return None, error_data

    def scrape_repo_list(self, repo_list, release_date=False):
        errors_data = None
        repos_data = None

        for repo_name in repo_list:
            repo_data, error_data = self.scrape_repo(
                repo_name=repo_name, release_date=release_date)
            if error_data is None:
                repos_data = pd.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                errors_data = pd.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
