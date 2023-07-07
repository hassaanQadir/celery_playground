from tasks import agent1, agent2, agent3, agent4, agent5, extract, process_results, complete
from celery import group, chain, chord
import json
import time

def run_chord(inputList, agent):
    # The header of the chord consists of a list of tasks connected by a pipeline (the '|' operator)
    # Each task in the list is created by calling 's()' (which stands for 'signature') on the task function
    # and passing the phase as an argument. The output from each task in the pipeline is passed to the next task.
    chord_header = [agent.s(phase) | extract.s() for phase in inputList]

    # The callback is a task that will be run once all tasks in the group have finished
    # The arguments to the callback task are the results from all the tasks in the group
    callback = process_results.s()

    # The chord is created by calling 'chord()' with the group of tasks and the callback
    # The chord is run when you call it
    result = chord(chord_header)(callback)

    # Once all tasks in the group are finished, the result from the callback task can be retrieved by calling 'get()'
    outputList = result.get()

    return outputList

def displayOutput(list1, list2, list3, list4, list5):
    data = {}

    for phase in list1:
        data[phase] = {}

        for step in list2:
            # this is where we sequentially call the OpenAI API
            # step = complete(step)
            data[phase][step] = {}

            for substep in list3:
                data[phase][step][substep] = {}

                for command in list4:
                    data[phase][step][substep][command] = []

                    for API_call in list5:
                        data[phase][step][substep][command] = [API_call]
    
    return data

def driver(user_input):
    phaseList = []
    stepList = []
    substepList = []
    commandList = []
    API_call_list = []
    data = {}

    # here we take the user input and pass it to agent1 to create a list of three phases
    phases = agent1.delay(user_input).get()
    newPhaseList = extract.delay(phases).get()
    phaseList.extend(newPhaseList)

    # we use Celery chords to run multiple parallel instances of a given agent
    # then pass the results to a chord which runs multiple instances of the next agent
    stepList = run_chord(phaseList, agent2)
    substepList = run_chord(stepList, agent3)
    commandList = run_chord(substepList, agent4)
    API_call_list = run_chord(commandList, agent5)

    # now that we've created all the output,
    # we pass it to a function which puts it in a nested dictionary to print out to display it
    data = displayOutput(phaseList, stepList, substepList, commandList, API_call_list)
    print(json.dumps(data, indent=4))

    return data
    
    
driver("Make glow in the dark E. coli")







