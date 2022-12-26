from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # USER-BROWSING SIMULATION FOR ISSUES ENDPOINT
    @task(2)
    def view_issues(self):
        self.client.get('/publication/issues', name='/publication/issues')

    @task(4)
    def view_issue(self):
        issue_id = randint(1, 100)
        self.client.get(
            f'/publication/issues/{issue_id}',
            name='/publication/issues/:id'
        )

    # USER-BROWSING SIMULATION FOR ARTICLES ENDPOINT
    @task(2)
    def view_articles(self):
        self.client.get('/publication/articles', name='/publication/articles')

    @task(4)
    def view_article(self):
        article_id = randint(1, 1000)
        self.client.get(
            f'/publication/articles/{article_id}',
            name='/publication/articles/:id'
        )

    # USER-BROWSING SIMULATION FOR MEMBERS ENDPOINT
    @task(2)
    def view_members(self):
        self.client.get('/publication/members', name='/publication/members')

    @task(2)
    def view_member(self):
        member_id = randint(1, 2)
        self.client.get(
            f'/publication/members/{member_id}',
            name='/publication/members/:id'
        )
