
import pandas as pd
import numpy as np
import time


class GitHubDiscussion:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.implicitly_wait(5)


    # def mine_repos(self, repo_list):
    #     post_list = pd.DataFrame()
        
    #     for repo in repo_list:
    #         posts = self.mine_repo(repo)
    #         post_list = pd.concat([post_list, posts], ignore_index=True)
    #         time.sleep(5)
            
    #     return post_list


    def mine_repo(self, repo):
        self.driver = uc.Chrome()
        self.driver.implicitly_wait(5)
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
            time.sleep(1)

        posts = pd.DataFrame()
        for url in posts_url_lst:
            post = self.get_data(url)
            post = pd.DataFrame([post])
            posts = pd.concat([posts, post], ignore_index=True)
            time.sleep(1)
            
        return posts
            

    def convert2num(self, num):
        try:
            return int(num)
        except:
            try:
                return int(num.strip().split()[0])
            except:
                return 0


    def get_data(self, url):
        self.driver.get(url)

        post = {}

        # question_title
        title = self.driver.find_element(
            By.XPATH, '//span[@class="js-issue-title markdown-title"]').text
        # print("Title:", title)
    
        # question_tag_count
        tag_count = len(self.driver.find_elements(By.XPATH, '//span[@class="discussion-sidebar-item js-discussion-sidebar-item"]/div[1]/a'))
        # print("tag_count:", tag_count)

        # Question_created_time
        date = self.driver.find_element(
            By.XPATH, '//relative-time[@class="no-wrap"]').get_attribute("datetime")
        # print("date:", date)

        # Question_score_count
        upvote_count = self.driver.find_element(
            By.XPATH, '//div[@class="text-center discussion-vote-form position-relative"]//button').text
        upvote_count = self.convert2num(upvote_count)
        # print("Question_score_count:", upvote_count)

        # question_body
        body = self.driver.find_element(
            By.XPATH, '//td[@class="d-block color-fg-default comment-body markdown-body js-comment-body"]').get_attribute("innerText").strip()
        # print("body:", body)

        # question_answer_count
        answer_count = self.driver.find_element(
            By.XPATH, '//h2[@id="discussion-comment-count"]/span[1]')
        answer_count = self.convert2num(answer_count)
        # print("answer_count:", len(answers_lst))

        post["Question_title"] = title
        post["Question_tag_count"] = tag_count
        post["Question_link"] = url
        post["Question_created_time"] = date
        post["Question_answer_count"] = answer_count
        post["Question_score_count"] = upvote_count
        post["Question_body"] = body
        post['Question_closed_time'] = np.nan
        post['Answer_score_count'] = np.nan
        post['Answer_comment_count'] = np.nan
        post['Answer_body'] = np.nan
        post["Question_self_closed"] = np.nan
    
        info = self.driver.find_element(By.XPATH, '//div[@class="d-flex flex-wrap flex-items-center mb-3 mt-2"]')
        accepted = info.find_element(By.XPATH, './/span').get_attribute('title')
    
        if accepted == 'Answered':
            answer = self.driver.find_element(By.XPATH, '//section[@class="width-full" and @aria-label="Marked as Answer"]')
            post['Question_closed_time'] = answer.find_element(By.XPATH, './/relative-time').get_attribute('datetime')
            Answer_score_count = answer.find_element(By.XPATH, './/div[@class="text-center discussion-vote-form position-relative"]//button').text
            post['Answer_score_count'] = self.convert2num(Answer_score_count)
            post['Answer_body'] = answer.find_element(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body"]').get_attribute('innerText').strip()
            comments = answer.find_elements(By.XPATH, './/td[@class="d-block color-fg-default comment-body markdown-body js-comment-body px-3 pt-0 pb-2"]/p')
            post['Answer_comment_count'] = len(comments)
            post['Answer_comment_body'] = ' '.join([comment.get_attribute('innerText').strip() for comment in comments])
            answerer = info.find_element(By.XPATH, './/a[@class="Link--secondary text-bold"]').text
            poster = info.find_element(By.XPATH, './/a[@class="Link--secondary text-bold d-inline-block"]').get_attribute('innerText').strip()
            post['Question_self_closed'] = poster == answerer

        return post


    def get_url(self, url):
        self.driver.get(url)

        posts_url = set()
        post_list = self.driver.find_elements(
            By.XPATH, '//div[@class="lh-condensed pl-2 pr-3 flex-1"]/h3/a')

        for post in post_list:
            posts_url.add(post.get_attribute('href'))

        return posts_url
    