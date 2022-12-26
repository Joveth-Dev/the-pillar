# from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
# from templated_mail.mail import BaseEmailMessage
from .tasks import notify_readers
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
import requests


class HelloView(APIView):
    @method_decorator(cache_page(1))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': data})


# @cache_page(5 * 60)
def say_hello(request):
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()
    notify_readers.delay('Hello')
    # THE IS FOR SENDING EMAILS TO USER IN DEVELOPMENT
    # try:
    # send_mail(subject='subject',
    #           message='message',
    #           html_message='message',
    #           from_email='joveth@domain.com',
    #           recipient_list=['kizzelyn@domain.com'])
    # mail_admins(subject='subject',
    #             message='message',
    #             html_message='message')
    # email = EmailMessage('subject', 'message', 'joveth@domain.com', ['kizzelyn@domain.com'])
    # email.attach_file('playground/static/images/Night Sky.jpg')
    # email.send()
    #     mail = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Joveth'}
    #     )
    #     mail.send(to=['Kizzelyn@domain.com'])
    # except BadHeaderError:
    #     raise BadHeaderError
    return render(request, 'hello.html', {'name': 'Joveth'})
