from requests import post
from celery_worker import app


def task_time(secs: str):
    print(secs)
    url = 'https://gttb.guane.dev/api/workers?task_complexity='+secs
    response = post(url)
    return response.json()

@app.task()
def complex_task(secs: str):
    print("In")
    response = task_time(secs=secs)
    print(response)
    print("Out")

