from selenium.webdriver.common.by import By
from github import Github

import undetected_chromedriver as uc
import pandas as pd
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
                
                if pd.notna(issue.closed_at):
                    try:
                        issue_data['Issue_self_closed'] = issue.closed_by.id == issue.user.id
                    except:
                        issue_data['Issue_self_closed'] = False
                    comments = []
                    upvotes = []
                    downvotes = []
                    for comment in issue.get_comments():
                        time.sleep(3)
                        comments.append(comment.body)
                        reactions = comment.get_reactions()
                        upvote = sum(reaction.content == '+1' for reaction in reactions)
                        downvote = sum(reaction.content == '-1' for reaction in reactions)
                        upvotes.append(upvote)
                        downvotes.append(downvote)
                    issue_data['Issue_comment_body'] = ' '.join(comments)
                    issue_data['Issue_comment_upvote'] = sum(upvotes)
                    issue_data['Issue_comment_downvote'] = sum(downvotes)
                    
                issue_data = pd.DataFrame([issue_data])
                issues_data = pd.concat(
                    [issues_data, issue_data], ignore_index=True)

        return issues_data

    def scrape_issue_list(self, repo_list):
        issues_data_list = pd.DataFrame()

        for repo_name in repo_list:
            print(f'Scraping {repo_name}')
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

        except Exception as e:
            print(f'Repo: {repo_name}, Error: {e}')
            return pd.DataFrame()

    def scrape_repo_list(self, repo_list):
        repos_data = pd.DataFrame()

        for repo_name in repo_list:
            print(f'Scraping {repo_name}')
            repo_data = self.scrape_repo(repo_name=repo_name)
            repos_data = pd.concat([repos_data, repo_data], ignore_index=True)

        return repos_data

    def scrape_discussion(self, repo):
        self.driver = uc.Chrome()
        self.driver.implicitly_wait(4)
        
        base_url = f'https://github.com/{repo}/discussions/categories/q-a?page='
        posts_url_lst = set()
        index = 0

        while True:
            index += 1
            page_url = base_url + str(index)
            posts_url = self.get_url(page_url)

            if not posts_url:
                break
        
            posts_url_lst = posts_url_lst.union(posts_url)

        posts = pd.DataFrame()
        for url in posts_url_lst:
            post = self.get_data(url)
            if not post:
                continue
            posts = pd.concat([posts, pd.DataFrame([post])], ignore_index=True)
            
        self.driver.close()
        self.driver.quit()
        return posts
            
    def convert2num(self, num):
        try:
            return int(num)
        except:
            try:
                return int(num.strip().split()[0])
            except:
                try:
                    return int(num.strip().split()[-1])
                except:
                    return 0

    def get_data(self, url):
        self.driver.get(url)

        post = {}

        try:
            # question_title
            title = self.driver.find_element(
                By.XPATH, '//span[@class="js-issue-title markdown-title"]').text
            # print("Title:", title)
        except:
            print(url)
            return post
            
        # question_tag_count
        tag_count = len(self.driver.find_elements(By.XPATH, '//div[@class="discussion-sidebar-item js-discussion-sidebar-item"]/div[2]/a'))
        # print("tag_count:", tag_count)

        # Question_created_time
        date = self.driver.find_element(
            By.XPATH, '//relative-time[@class="no-wrap"]').get_attribute("datetime")
        # print("date:", date)

        # Question_score_count
        upvote_count = self.driver.find_element(
            By.XPATH, '//div[@class="text-center discussion-vote-form position-relative"]//button').get_attribute('aria-label')
        upvote_count = self.convert2num(upvote_count)
        # print("Question_score_count:", upvote_count)

        # question_body
        body = self.driver.find_element(
            By.XPATH, '//td[@class="d-block color-fg-default comment-body markdown-body js-comment-body"]').get_attribute("innerText").strip()
        # print("body:", body)

        # question_answer_count
        answer_count = self.driver.find_element(
            By.XPATH, '//h2[@id="discussion-comment-count"]/span[2]').get_attribute("innerText").strip()
        answer_count = self.convert2num(answer_count)
        # print("answer_count:", len(answers_lst))

        post["Question_title"] = title
        post["Question_tag_count"] = tag_count
        post["Question_link"] = url
        post["Question_created_time"] = date
        post["Question_answer_count"] = answer_count
        post["Question_score_count"] = upvote_count
        post["Question_body"] = body
    
        info = self.driver.find_element(By.XPATH, '//div[@class="d-flex flex-wrap flex-items-center mb-3 mt-2"]')
        accepted = info.find_element(By.XPATH, './/span').get_attribute('title')
    
        if accepted == 'Answered':
            answerer = info.find_element(By.XPATH, './/a[@class="Link--secondary text-bold"]').text
            poster = info.find_element(By.XPATH, './/a[@class="Link--secondary text-bold d-inline-block"]').get_attribute('innerText').strip()
            post['Question_self_closed'] = poster == answerer
            answer = self.driver.find_element(By.XPATH, '//section[@class="width-full" and @aria-label="Marked as Answer"]')
            post['Question_closed_time'] = answer.find_element(By.XPATH, './/relative-time').get_attribute('datetime')
            comments = answer.find_elements(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body px-3 pt-0 pb-2"]/p')
            post['Answer_comment_count'] = len(comments)
            post['Answer_comment_body'] = ' '.join([comment.get_attribute('innerText').strip() for comment in comments])
            try:
                Answer_score_count = answer.find_element(By.XPATH, './/div[@class="text-center discussion-vote-form position-relative"]//button').get_attribute('aria-label')
                post['Answer_score_count'] = self.convert2num(Answer_score_count)
                try:
                    post['Answer_body'] = answer.find_element(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body"]').get_attribute('innerText').strip()
                except:
                    post['Answer_body'] = answer.find_element(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body email-format"]/div').get_attribute('innerText').strip()
            except:
                post['Answer_body'] = answer.find_element(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body px-3 pt-0 pb-2"]').get_attribute('innerText').strip()

        return post

    def get_url(self, url):
        self.driver.get(url)

        posts_url = set()
        post_list = self.driver.find_elements(
            By.XPATH, '//div[@class="lh-condensed pl-2 pr-3 flex-1"]/h3/a')

        for post in post_list:
            posts_url.add(post.get_attribute('href'))

        return posts_url
    