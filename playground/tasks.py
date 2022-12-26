from time import sleep
from celery import shared_task


@shared_task
def notify_readers(message):
    print('Greeting 10k readers...')
    print(message)
    sleep(10)
    print('Greetings were succesfully sent!')
