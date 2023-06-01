from github import Github
import pandas as pd
import numpy as np
import time


def sleep_wrapper(func, *args, **kwargs):
    time.sleep(3)
    return func(*args, **kwargs)


class GitHubMiner:
    def __init__(self, private_token):
        self.github = Github(login_or_token=private_token)

    def scrape_issue(self, repo_name):
        repo = sleep_wrapper(self.github.get_repo, full_name_or_id=repo_name)
        n_contributors = sleep_wrapper(repo.get_contributors).totalCount
        issues = sleep_wrapper(repo.get_issues, state='all')
        issues_data = pd.DataFrame()

        for issue in issues:
            time.sleep(3)
            if not issue.pull_request:
                issue_data = {}
                issue_data['Issue_link'] = issue.html_url
                issue_data['Issue_title'] = issue.title
                issue_data['Issue_label'] = [
                    label.name for label in issue.labels]
                issue_data['Issue_created_time'] = issue.created_at
                issue_data['Issue_closed_time'] = issue.closed_at
                reactions = issue.get_reactions()
                issue_data['Issue_upvote_count'] = sum(
                    reaction.content == '+1' for reaction in reactions)
                issue_data['Issue_downvote_count'] = sum(
                    reaction.content == '-1' for reaction in reactions)
                issue_data['Issue_body'] = issue.body
                issue_data['Issue_comment_count'] = issue.comments
                issue_data['Issue_repo_issue_count'] = issues.totalCount
                issue_data['Issue_repo_watch_count'] = repo.subscribers_count
                issue_data['Issue_repo_star_count'] = repo.stargazers_count
                issue_data['Issue_repo_fork_count'] = repo.forks
                issue_data['Issue_repo_contributor_count'] = n_contributors
                issue_data['Issue_self_closed'] = np.nan
                issue_data['Comment_body'] = np.nan
                if pd.notna(issue.closed_at):
                    issue_data['Issue_self_closed'] = issue.closed_by.id == issue.user.id
                    issue_data['Comment_body'] = ' '.join([comment.body for comment in issue.get_comments()])
                issue_data = pd.DataFrame([issue_data])
                issues_data = pd.concat(
                    [issues_data, issue_data], ignore_index=True)

        return issues_data

    def scrape_issue_list(self, repo_list):
        issues_data_list = pd.DataFrame()

        for repo_name in repo_list:
            issues_data = self.scrape_issue(repo_name=repo_name)
            issues_data_list = pd.concat(
                [issues_data_list, issues_data], ignore_index=True)

        return issues_data_list

    def scrape_repo(self, repo_name, real_name=None, release_time=None):
        try:
            repo = sleep_wrapper(self.github.get_repo,
                                 full_name_or_id=repo_name)
            commits = sleep_wrapper(repo.get_commits)
            releases = sleep_wrapper(repo.get_releases)
            issues = sleep_wrapper(repo.get_issues, state='all')

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Repo Created Date': repo.created_at,
                'Last Commit Date': commits[0].commit.author.date,
                'Topic': sleep_wrapper(repo.get_topics),
                'Language': repo.language,
                'Size': repo.size,
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Contributor': sleep_wrapper(repo.get_contributors).totalCount,
                '#Branch': sleep_wrapper(repo.get_branches).totalCount,
                '#Release': releases.totalCount,
                '#Commit': commits.totalCount,
                '#Pull Requests': sleep_wrapper(repo.get_pulls, state='all').totalCount,
                '#Pull Requests (Open)': sleep_wrapper(repo.get_pulls, state='open').totalCount,
                '#Issue': issues.totalCount,
                '#Issue (Open)': sleep_wrapper(repo.get_issues, state='open').totalCount
            }

            if real_name:
                repo_data['Name'] = real_name

            if release_time:
                repo_data['First Release Date'] = release_time
            elif repo_data['#Release']:
                repo_data['First Release Date'] = releases.reversed[0].created_at

            repo_data = pd.DataFrame([repo_data])
            return repo_data

        except Exception as err:
            print(f'Repo: {repo_name}, Error: {err.status}')
            return pd.DataFrame()

    def scrape_repo_list(self, repo_list):
        repos_data = pd.DataFrame()

        for repo_name in repo_list:
            repo_data = self.scrape_repo(repo_name=repo_name)
            repos_data = pd.concat([repos_data, repo_data], ignore_index=True)

        return repos_data
