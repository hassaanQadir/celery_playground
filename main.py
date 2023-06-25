from tasks import agent1, agent2, agent3, agent4, askOpenTrons, extract, process_results, complete
from celery import group, chain, chord
import json

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


def driver(user_input):
    phaseList = []
    stepList = []
    substepList = []
    commandList = []
    API_call_list = []
    data = {}

    phases = agent1(user_input)
    newPhaseList = extract(phases)
    phaseList.extend(newPhaseList)
   
    stepList = run_chord(phaseList, agent2)
    substepList = run_chord(stepList, agent3)
    commandList = run_chord(substepList, agent4)
    API_call_list = run_chord(commandList, agent5)

    for phase in phaseList:
        data[phase] = {}

        for step in stepList:
            step = complete(step)
            data[phase][step] = {}

            for substep in substepList:
                data[phase][step][substep] = {}

                for command in commandList:
                    data[phase][step][substep][command] = []

                    for API_call in API_call_list:
                        data[phase][step][substep][command] = [API_call]
    
    print(json.dumps(data, indent=4))
    return data
    
    
driver("Make glow in the dark E. coli")







