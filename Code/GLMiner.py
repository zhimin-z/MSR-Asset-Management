import gitlab
import operator
import pandas


class GitlabMiner():
    def __init__(self, token):
        self.gitlab = gitlab.Gitlab(private_token=token)
        self.repo_columns = [
            'Repo',
            'Link',
            'Archived',
            'Creation Date',
            '#Star',
            '#Fork',
            '#Commits',
            '#Branches',
            'Topics',
            '#Releases',
            '#Member',
            '#Open Issues',
            '#Merge Requests',
            'Language'
        ]
        self.error_columns = [
            'Repo',
            'Error'
        ]

    def scrape(self, repo_name, name=None, date=None, real_creation_date=True):
        try:
            project = self.gitlab.projects.get(repo_name)

            creation_date = project.created_at
            if not real_creation_date:
                creation_date = project.commits.list(all=True)[-1].created_at

            if date is not None:
                last_commit_date = project.commits.list(all=True)[0].created_at
                if date > last_commit_date:
                    error_data = {'Repo': repo_name, 'Error': 'Unrelated'}
                    error_data = pandas.DataFrame([error_data])
                    return None, error_data

            repo_data = {
                'Repo': repo_name,
                'Link': project.http_url_to_repo,
                'Archived': project.archived,
                'Creation Date': creation_date,
                '#Star': project.star_count,
                '#Fork': project.forks_count,
                '#Commits': len(project.commits.list(all=True)),
                '#Branches': len(project.branches.list(all=True)),
                'Topics': project.topics,
                '#Releases': len(project.releases.list(all=True)),
                '#Member': len(project.members.list(all=True)),
                '#Open Issues': len(project.issues.list(all=True, state='opened')),
                'Language': max(project.languages().items(), key=operator.itemgetter(1))[0]
            }

            try:
                repo_data['#Merge Requests'] = len(
                    project.mergerequests.list(all=True, state='opened'))
            except Exception as err:
                repo_data['#Merge Requests'] = 0

            if name is not None:
                repo_data['Name'] = name

            repo_data = pandas.DataFrame([repo_data])

        except Exception as err:
            error_data = {'Repo': repo_name, 'Error': str(err)}
            error_data = pandas.DataFrame([error_data])
            return None, error_data

        return repo_data, None

    def collect(self, repo_names, name=None, date=None, real_creation_date=True):
        repos_data = pandas.DataFrame(columns=self.repo_columns)
        errors_data = pandas.DataFrame(columns=self.error_columns)

        for repo_name in repo_names:
            repo_data, error_data = self.scrape(
                repo_name=repo_name, name=name, date=date, real_creation_date=real_creation_date)

            if error_data is None:
                repos_data = pandas.concat(
                    [repos_data, repo_data], ignore_index=True)
            else:
                errors_data = pandas.concat(
                    [errors_data, error_data], ignore_index=True)

        return repos_data, errors_data
