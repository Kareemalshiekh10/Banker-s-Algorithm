#Banker's Algorithm
import PySimpleGUI as psg

psg.theme('DarkTanBlue')

#Processes and Resources
layout = [[psg.Text('Number Of Processes:')], [psg.InputText()]]
layout.append( [[psg.Text('Number Of Resources:')], [psg.InputText()],[psg.Button('Ok')]])

window = psg.Window('Processes and Resources', layout)
event, values = window.read()
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    elif event == 'Ok':
        NoOfProcesses = int(values[0])
        NoOfResources = int(values[1])
        window.close()
        break

#Total Available Resources
layout=[[psg.Text('Total Available Resources:')], [psg.InputText()], [psg.Button('Ok')]]
window = psg.Window('Total Available Resources', layout)
event, values = window.read()
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    elif event == 'Ok':
       Available = list(map(int,values[0].split()))
       if len(Available) != NoOfResources:
           psg.popup("Error: The number of resources entered must match the number of resources specified earlier.")
       else:
           window.close()
           break

#allocation matrix 
layout = [[psg.Text('Allocation Matrix:')]]
for i in range(NoOfProcesses):
    layout.append([psg.InputText()])
layout.append([psg.Button('Ok')])
window = psg.Window('Allocation Matrix', layout)
event, values = window.read()
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    elif event == 'Ok':
       allocationRes = []
       for i in range(NoOfProcesses):
           row = list(map(int, values[i].split()))
           if len(row) != NoOfResources:
               psg.popup("Error: The number of resources entered must match the number of resources specified earlier.")
               allocationRes = []
               break
           else:
               allocationRes.append(row)
       if allocationRes:
           window.close()
           break

#Max Need
layout = [[psg.Text('Max Need:')]]
for i in range(NoOfProcesses):
    layout.append([psg.InputText()])
layout.append([psg.Button('Ok')])
window = psg.Window('Max Need', layout)
event, values = window.read()
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    elif event == 'Ok':
       MaxNeed = []
       for i in range(NoOfProcesses):
           row = list(map(int, values[i].split()))
           if len(row) != NoOfResources:
               psg.popup("Error: The number of resources entered must match the number of resources specified earlier.")
               MaxNeed = []
               break
           else:
               MaxNeed.append(row)
       if MaxNeed:
           window.close()
           break

def banker_algorithm(NoOfProcesses, NoOfResources, allocationRes, MaxNeed, Available):
    # Initialize the needed and finish matrices
    needed = [[MaxNeed[i][j] - allocationRes[i][j] for j in range(NoOfResources)] for i in range(NoOfProcesses)]
    finish = [False] * NoOfProcesses

    # Iterate until all processes are finished or no more processes can be allocated
    while False in finish:
        safe_state_found = False

        # Check if a process can be safely allocated resources
        for i in range(NoOfProcesses):
            if not finish[i]:
                if all(needed[i][j] <= Available[j] for j in range(NoOfResources)):
                    # Allocate resources to the process
                    for j in range(NoOfResources):
                        Available[j] += allocationRes[i][j]

                    # Mark the process as finished and update the safe state flag
                    finish[i] = True
                    safe_state_found = True

        # If no safe state was found during the last iteration, exit the loop
        if not safe_state_found:
            break

    return not (False in finish)

# Request Resources from a Process
layout = [[psg.Text('Enter the request details:')], [psg.Text('Process Index: '), psg.InputText(key='process_index')], [psg.Text('Resource Index: '), psg.InputText(key='resource_index')],[psg.Text('Request Quantity: '), psg.InputText(key='request_quantity')], [psg.Button('Request')]]
window = psg.Window('Request Resources', layout)
event, values = window.read()
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    elif event == 'Request':
        process_index = int(values['process_index'])
        resource_index = int(values['resource_index'])
        request_quantity = int(values['request_quantity'])

    # Check if the request is valid
    if request_quantity <= Available[resource_index] and request_quantity <= MaxNeed[process_index][resource_index] - allocationRes[process_index][resource_index]:
        # Simulate the allocation of resources to the process
        temp_available = Available.copy()
        temp_allocation = [row.copy() for row in allocationRes]
        temp_needed = [row.copy() for row in needed]

        temp_available[resource_index] -= request_quantity
        temp_allocation[process_index][resource_index] += request_quantity
        temp_needed[process_index][resource_index] -= request_quantity

        # Check if the new state is safe
        if banker_algorithm(NoOfProcesses, NoOfResources, temp_allocation, temp_needed, temp_available):
            Available = temp_available
            allocationRes = temp_allocation
            needed = temp_needed

            psg.popup("The request can be granted. The system is in a safe state.")
        else:
            psg.popup("The request cannot be granted. It will result in an unsafe state.")
    else:
        psg.popup("Invalid request. The requested quantity is greater than what is available or what the process needs.")
        window.close()



# Run the banker's algorithm on the input data and display the results in a popup window
if banker_algorithm(NoOfProcesses, NoOfResources, allocationRes, MaxNeed, Available):
    psg.popup("The system is in a safe state.")
else:
    psg.popup("The system is in an unsafe state.")
