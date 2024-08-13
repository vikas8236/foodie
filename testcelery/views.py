

import logging
from django.http import HttpResponse
from testcelery.tasks import print_message


def test_celery(request):
    message_result = print_message.delay('Hello from Django view!')
    return HttpResponse(message_result)

