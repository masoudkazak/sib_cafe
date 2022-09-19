from celery import shared_task


@shared_task
def create_rate_task(user, food, value):
    print("Hiiiiiiiiiii")
