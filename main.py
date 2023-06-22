from tasks import add, chain1, chain2
import time

result = add.delay(40, 6)
print(result.ready())  # Should print False, task may not have completed.

i = 0

while i < 5:
    print(i)
    time.sleep(1)
    i += 1
    try:
        print(result.get(timeout=1))  # Will print the answer if the task is done.
    except:
        print("Task not done yet.")
    

def driver(user_input):
    output_string = ""

    phase = chain1.delay(user_input).get() # Block until the task is done and get the result.
    
    step1 = chain2.delay(phase, 1).get()  # Block until the task is done and get the result.
    step2 = chain2.delay(phase, 2).get()  # Block until the task is done and get the result.
    step3 = chain2.delay(phase, 3).get()  # Block until the task is done and get the result.

    output_string += str(phase)
    output_string += str(step1)
    output_string += str(step2)
    output_string += str(step3)

    print(output_string)
    return output_string

driver("Make glow in the dark E. coli")
