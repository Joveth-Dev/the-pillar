from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def register_user(self):
        username_number = randint(1, 10000000000)
        password_number = randint(1, 10000000000)
        email_number = randint(1, 10000000000)
        self.client.post(
            '/auth/users',
            name='/auth/users',
            json={
                'username': f'dummyuser{username_number}',
                'password': f'ILoveDjango{password_number}',
                'email': f'dummy{email_number}@domain.com',
                'last_name': 'Dummy',
                'first_name': 'Dummy',
                'middle_initial': 'D'
            })
    # def sign_in_user(self):
    #     self.client.get('')

    # NO DOWNLOAD FUNCTION YET
    # def download_article(self):
    #     pass
