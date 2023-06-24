from tasks import layer1, layer2, layer3, agent1, agent2, agent3, agent4, askOpenTrons, extract
from celery import group, chain
import json

def driver1(user_input):
    output_string = ""

    phase = layer1.delay(user_input).get() # Block until the task is done and get the result.
    
    step1 = layer2.delay(phase, 1).get()  # Block until the task is done and get the result.
    step2 = layer2.delay(phase, 2).get()  # Block until the task is done and get the result.
    step3 = layer2.delay(phase, 3).get()  # Block until the task is done and get the result.

    step4 = layer3.delay(step1, 4).get()  # Block until the task is done and get the result.
    step5 = layer3.delay(step1, 5).get()  # Block until the task is done and get the result.
    step6 = layer3.delay(step1, 6).get()  # Block until the task is done and get the result.

    step7 = layer3.delay(step2, 7).get()  # Block until the task is done and get the result.
    step8 = layer3.delay(step2, 8).get()  # Block until the task is done and get the result.
    step9 = layer3.delay(step2, 9).get()  # Block until the task is done and get the result.

    step10 = layer3.delay(step3, 10).get()  # Block until the task is done and get the result.
    step11 = layer3.delay(step3, 11).get()  # Block until the task is done and get the result.
    step12 = layer3.delay(step3, 12).get()  # Block until the task is done and get the result.

    output_string += str(phase)
    output_string += str(step1)
    output_string += str(step2)
    output_string += str(step3)
    output_string += str(step4)
    output_string += str(step5)
    output_string += str(step6)
    output_string += str(step7)
    output_string += str(step8)
    output_string += str(step9)
    output_string += str(step10)
    output_string += str(step11)
    output_string += str(step12)

    print(output_string)
    return output_string


def driver2(user_input):
    output_string = ""

    # Run layer1 task
    phase = layer1.delay(user_input).get()  # Block until the task is done and get the result.

    # Prepare a group of layer2 tasks, each chained with a group of layer3 tasks
    g = group(
        chain(layer2.s(phase, i), group(layer3.s(j) for j in range(1, 4)))
        for i in range(1, 4)
    )
    
    # Run the group of tasks and get the results
    results = g.apply_async().get()
    # Create the output string
    output_string += str(phase)

    for result in results:
        output_string += str(result)
    
    print(output_string)
    return output_string

def driver3(user_input):
    phaseList = []
    stepList = []
    substepList = []
    commandList = []
    API_call_list = []
    
    phases = agent1(user_input)
    newPhaseList = extract(phases)
    phaseList.extend(newPhaseList)
   
    for phase in phaseList:
        steps = agent2(phase)
        newStepList = extract(steps)
        stepList.extend(newStepList)
    
    for step in stepList:
        substeps = agent3(step)
        newSubstepList = extract(substeps)
        substepList.extend(newSubstepList)

    for substep in substepList:
        commands = agent4(substep)
        newCommandList = extract(commands)
        commandList.extend(newCommandList)
    
    for command in commandList:
        API_calls = askOpenTrons(command)
        new_API_call_list = extract(API_calls)
        API_call_list.extend(new_API_call_list)
    data = {}

    for phase in phaseList:
        data[phase] = {}

        for step in stepList:
            data[phase][step] = {}

            for substep in substepList:
                data[phase][step][substep] = {}

                for command in commandList:
                    data[phase][step][substep][command] = []

                    for API_call in API_call_list:
                        data[phase][step][substep][command] = [API_call]
    
    print(json.dumps(data, indent=4))
    return data
    
    # then I should add a sleep to get a time
    # then I need to use celery to group each layer and it should get way faster
    # then I should add a simple OpenAI API call and see if that blows up
    # and probably I'll have to figure out how to use the openai-multi-client library

driver3("Make glow in the dark E. coli")








