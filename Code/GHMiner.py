from github import Github, GithubException
import pandas
import time


class GHMiner():
    def __init__(self, token):
        self.github = Github(token)
        self.repo_columns = ['Repo',
                             'Link',
                             'Archived',
                             'Creation Date',
                             'Topics',
                             '#Star',
                             '#Watch',
                             '#Fork',
                             '#Releases',
                             '#Contributors',
                             'Languages',
                             'Size',
                             '#Open Issues',
                             '#Pull Requests',
                             '#Branches',
                             '#Tags',
                             '#Commits',
                             '#Comments',
                             '#Downloads',
                             '#Deployments']
        self.error_columns = ['Repo', 'Error']

    def scrape(self, repo_name, name=None, date=None, real_creation_date=True):
        try:
            repo = self.github.get_repo(repo_name)

            if repo.fork:
                error_data = {'Repo': repo_name, 'Error': 'Fork'}
                return None, error_data

            creation_date = repo.created_at
            if not real_creation_date:
                creation_date = repo.get_commits(
                ).reversed[0].commit.author.date

            if date is not None and date >= creation_date:
                error_data = {'Repo': repo_name, 'Error': 'Unrelated'}
                return None, error_data

            repo_data = {
                'Repo': repo_name,
                'Link': repo.html_url,
                'Archived': repo.archived,
                'Creation Date': creation_date,
                'Topics': repo.get_topics(),
                '#Star': repo.stargazers_count,
                '#Watch': repo.subscribers_count,
                '#Fork': repo.forks,
                '#Releases': repo.get_releases().totalCount,
                '#Contributors': repo.get_contributors().totalCount,
                'Languages': repo.language,
                'Size': repo.size,
                '#Open Issues': repo.open_issues_count,
                '#Pull Requests': repo.get_pulls().totalCount,
                '#Branches': repo.get_branches().totalCount,
                '#Tags': repo.get_tags().totalCount,
                '#Commits': repo.get_commits().totalCount,
                '#Comments': repo.get_comments().totalCount,
                '#Downloads': repo.get_downloads().totalCount,
                '#Deployments': repo.get_deployments().totalCount,
                # 'Open Issue': repo.get_issues(state='open'),
                # 'Branch': repo.get_branches(),
                # 'Projects': repo.get_projects(),
                # 'Milestone': repo.get_milestones(state='open'),
            }

            if name is not None:
                repo_data['Name'] = name

        except GithubException as err:
            error_data = {'Repo': repo_name, 'Error': err.data['message']}
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

            time.sleep(10)

        return repos_data, errors_data
