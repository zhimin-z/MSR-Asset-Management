from gitlab import Gitlab
import pandas as pd
import operator
import time


class GitLabMiner():
    def __init__(self, private_token):
        self.gitlab = Gitlab(private_token=private_token)

    def scrape(self, repo_name, tool_release_date=None):
        def sleep_wrapper(func, **args):
            time.sleep(0.1)
            return func(**args)
        
        try:
            repo = self.gitlab.projects.get(repo_name)

            commits = sleep_wrapper(repo.commits.list, get_all=True)
            last_commit_date = pd.to_datetime(
                commits[0].created_at).to_datetime64()
            if tool_release_date is not None and tool_release_date > last_commit_date:
                error_data = {'Repo': repo_name, 'Error': 'Unrelevant'}
                return None, error_data

            releases = sleep_wrapper(repo.releases.list, get_all=True)
            issues = sleep_wrapper(repo.issues.list, get_all=True, state='all')

            repo_data = {
                'Repo': repo_name,
                'Link': repo.http_url_to_repo,
                'Repo Creation Date': pd.to_datetime(repo.created_at).to_datetime64(),
                'Last Commit Date': last_commit_date,
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
            
            if len(issues) > 0:
                # An issue link example: https://gitlab.com/librespacefoundation/polaris/polaris/-/issues/30
                repo_data['#Issues (All)'] = issues[0].iid
            else:
                repo_data['#Issues (All)'] = 0

            if len(releases) > 0:
                repo_data['First Release Date'] = pd.to_datetime(releases[-1].created_at).to_datetime64()
                
            return repo_data, None

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': err}
            return None, error_data

    def collect(self, repo_list, tool_release_date=None):
        errors_data = None
        repos_data = None
        
        for repo_name in repo_list:
            repo_data, error_data = self.scrape(repo_name=repo_name, tool_release_date=tool_release_date)
            if error_data is None:
                repo_data = pd.DataFrame([repo_data])
                repos_data = pd.concat([repos_data, repo_data], ignore_index=True)
            else:
                error_data = pd.DataFrame([error_data])
                errors_data = pd.concat([errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
