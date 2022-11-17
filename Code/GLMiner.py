import gitlab
import operator
import pandas


class GitLabMiner():
    def __init__(self, private_token):
        self.gitlab = gitlab.Gitlab(private_token=private_token)
        self.repo_columns = [
            'Repo',
            'Link',
            'Creation Date',
            'First Activity Date',
            'Last Activity Date',
            'Language',
            'Topics',
            'Archived',
            '#Star',
            '#Fork',
            '#Issues',
            '#Commits',
            '#Branches',
            '#Releases',
            '#Member'
        ]
        self.error_columns = [
            'Repo',
            'Error'
        ]

    def scrape(self, repo_name, name=None, date=None):
        def sleep_wrapper(func, **args):
            return func(**args)
        try:
            project = self.gitlab.projects.get(repo_name)

            commits = sleep_wrapper(project.commits.list, all=True)
            last_commit_date = commits[0].created_at
            if date is not None and date > last_commit_date:
                error_data = {'Repo': repo_name, 'Error': 'Unrelevant'}
                return None, error_data

            repo_data = {
                'Repo': repo_name,
                'Link': project.http_url_to_repo,
                'Creation Date': project.created_at,
                'First Activity Date': commits[-1].created_at,
                'Last Activity Date': last_commit_date,
                'Language': max(sleep_wrapper(project.languages).items(), key=operator.itemgetter(1))[0],
                'Topics': project.topics,
                'Archived': project.archived,
                '#Star': project.star_count,
                '#Fork': project.forks_count,
                '#Issues': len(sleep_wrapper(project.issues.list, all=True)),
                '#Commits': len(sleep_wrapper(project.commits.list, all=True)),
                '#Branches': len(sleep_wrapper(project.branches.list, all=True)),
                '#Releases': len(sleep_wrapper(project.releases.list, all=True)),
                '#Member': len(sleep_wrapper(project.members.list, all=True))
            }

            try:
                repo_data['#Merge Requests'] = len(
                    sleep_wrapper(project.mergerequests.list, all=True))
            except Exception as err:
                repo_data['#Merge Requests'] = 0

            if name is not None:
                repo_data['Name'] = name

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': str(err)}
            return None, error_data

        return repo_data, None

    def collect(self, repo_names, name=None, date=None):
        repos_data = pandas.DataFrame(columns=self.repo_columns)
        errors_data = pandas.DataFrame(columns=self.error_columns)

        for repo_name in repo_names:
            repo_data, error_data = self.scrape(
                repo_name=repo_name, name=name, date=date)

            if error_data is None:
                repo_data = pandas.DataFrame([repo_data])
                repos_data = pandas.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                error_data = pandas.DataFrame([error_data])
                errors_data = pandas.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
