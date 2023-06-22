from celery import Celery
import time

app = Celery('tasks', backend='rpc://', broker='pyamqp://')


@app.task
def layer1(user_input):
    message = "Here is the user input: " + str(user_input) + "\n"
    message += "Let's break this into three phases\n"

    time.sleep(3)

    message += "Let's break each phase into steps\n"

    return message

@app.task
def layer2(phase, number):
    answer = "Phase #" + str(number) + " received : " + str(phase)[:10]
    time.sleep(3)
    answer += "Returning Phase #" + str(number) + "\n\n"
    return answer


@app.task
def layer3(phase, number):
    answer = "Step #" + str(number) + " received : " + str(phase)[:10]
    time.sleep(3)
    answer += "Returning Step #" + str(number) + "\n\n"
    return answer
