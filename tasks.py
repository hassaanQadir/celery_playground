from celery import Celery
import time
import re

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

@app.task
def agent1(input):
    answer = "We received", input, "and we output lePhase 1, lePhase 2, and lePhase 3"
    return answer

@app.task
def agent2(input):
    answer = "We received", input, "and we output theStep 1, theStep 2, and theStep 3"
    return answer

@app.task
def agent3(input):
    answer = "We received", input, "and we output Substep 1, Substep 2, and Substep 3"
    return answer

@app.task
def agent4(input):
    answer = "We received", input, "and we output Command 1, Command 2, and Command 3"
    return answer

@app.task
def agent1(input):
    answer = "We received", input, "and we output API code"
    return answer

@app.task
def extract_answers(s):
    # Match any number and get it with its preceding characters
    pattern = r'(.{0,9}\d+)'
    matches = re.findall(pattern, s)
    # Truncate each match to the last 9 characters plus the number
    answer = [match[-10:] for match in matches]
    # Remove the first entry from the list, which is just repeating the function's input
    cleanAnswer = answer[1:]
    return cleanAnswer

