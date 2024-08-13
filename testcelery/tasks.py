

from celery import shared_task
import time

# @shared_task

# def add(x, y):
    
#     import pdb; pdb.set_trace()
#     print("i'm inside task queue")
#     time.sleep(5)# Simulate a delay
#     return x + y

@shared_task
def print_message(message):
    print('i am also inside task queue')
    print(message)
    return message
