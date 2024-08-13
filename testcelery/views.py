

import logging
from django.http import HttpResponse
from testcelery.tasks import print_message

# Configure logging
# logger = logging.getLogger(__name__)
def test_celery(request):
    # import pdb; pdb.set_trace()
    # Log the start of the function
    # logger.info("test_celery view called")

    # Trigger the 'add' task
    # logger.info("Triggering 'add' task with arguments: 4, 6")
    # result = add.delay(4, 6)
    # logger.info(f"Task {result.task_id} sent. Waiting for result...")

    # Log before waiting for the result
    # logger.info("Waiting for task result...")
    # try:
    #     task_result = result.get(timeout=10)
        # logger.info(f"Task {result.task_id} completed with result: {task_result}")
    # except Exception as e:
        # logger.error(f"Error while getting task result: {e}")
        # return HttpResponse(f"Error while processing task: {str(e)}", status=500)

    # Trigger the 'print_message' task
    # logger.info("Triggering 'print_message' task with message: 'Hello from Django view!'")
    message_result = print_message.delay('Hello from Django view!')
    # logger.info("Message task sent")

    # Log the response
    # response_message = f'Task result: {task_result}'
    # logger.info(f"Returning response: {response_message}")
    
    return HttpResponse(message_result)

