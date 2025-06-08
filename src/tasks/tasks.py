from src.tasks.celery_app import celery_app


@celery_app.task
def resize_images(): ...
