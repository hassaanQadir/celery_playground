from celery import Celery
import time

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def add(x, y):
    time.sleep(5)
    return x + y + 100


@app.task
def chain1(user_input):
    message = "Here is the user input: " + str(user_input) + "\n"
    message += "Let's break this into three phases\n"

    time.sleep(3)

    message += "Phase 1 is Finding Genes\n"
    message += "Phase 2 is Making a Plasmid\n"
    message += "Phase 3 is Transforming E. coli\n"
    message += "Let's break this phase into steps\n"

    return message

@app.task
def chain2(phase, number):
    message = "Chain #" + str(number) + " received : " + str(phase)
    time.sleep(3)
    answer = "Returning Step #" + str(number) + "\n"
    message += answer
    return message
