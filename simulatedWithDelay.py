'''

Following code snippet implements Distributed Queuing

'''

import random, math, names, os, time, queue

class Client:

    ''' This class defines the basic structure of a Client'''

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __str__(self):
        return self.name


class ContentionSlots:

    ''' This class defines the basic structure of Contention Slots '''

    def __init__(self):
        self.number_of_slots = 5
        self.slots = {
            1:[],
            2:[],
            3:[],
            4:[],
            5:[]
        }


# Global Queues
DTQ = queue.Queue()
CRQ = queue.Queue()


# Helper Functions
def printDTQ (dtq):
    print("DTQ: ")
    for client in list(dtq.queue):
        print(client, end=", ")
    print(end="\n\n")


def printCRQ (crq):
    print("CRQ: ")
    for client_list in list(crq.queue):
        if len(client_list) is not 0:
            for client in client_list:
                print(client.name, end=", ")
            print()
    print(end="\n\n")


def printContentionSlots (contention_slots):
    print("Contention Slots: ")
    for slot, clients in contention_slots.slots.items():
        print(slot, end=": ")
        for client in clients:
            print(client.name, end=", ")
        print()
    print(end="\n\n")

def printAllowedClients (client_list):
    print("Clients allowed to contend: ", end="\n\n")
    for client in client_list:
        if client.status is True:
            print(client.name, end=", ")
    print(end="\n\n")

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def contention(client_list):

    '''
    This function initializes contention slots and asks the clients in client
    list to content for those slots randomly.
    '''

    # Print CRQ and DTQ first
    os.system('clear')
    printCRQ(CRQ)
    printDTQ(DTQ)

    if not DTQ.empty():
        client = DTQ.get()

        items = list(range(0, random.randint(1,50)))
        l = len(items)
        printProgressBar(0, l, prefix = client, suffix = 'Complete', length = 50)
        for i, item in enumerate(items):

            time.sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = client, suffix = 'Complete', length = 50)



    # Printing clients allowed to contend
    printAllowedClients(client_list)
    time.sleep(2)

    # Initialize contention slots
    contention_slots = ContentionSlots()

    # Ask clients to randomly content for slots and append clients to their contented slot lists.
    for client in client_list:
        if client.status is True:
            contented_slot = random.randint(1, 5)
            contention_slots.slots[contented_slot].append(client)

    # Print the contention slots
    printContentionSlots(contention_slots)
    time.sleep(5)


    # Return the contention slots to the calling function
    return contention_slots


def splitting(contention_slots):

    '''
    This function distributes the clients among DTQ and CRQ by evaluating the
    contention slot lists.
    '''

    # Distribute the clients in DTQ and CRQ
    for slot, client_list in contention_slots.slots.items():
        if len(client_list) is 1:
            DTQ.put(client_list[0])
        elif len(client_list) is 0:
            continue
        else:
            CRQ.put(client_list)

    if not CRQ.empty():
        resolution(CRQ, DTQ)

    return None


def resolution(CRQ, DTQ):

    os.system('clear')
    printCRQ(CRQ)
    printDTQ(DTQ)
    time.sleep(2)

    queue_element = CRQ.get()
    contention_slots = contention(queue_element)
    splitting(contention_slots)


def main():

    os.system('clear')

    client_list = []

    for i in range(20):
        name = names.get_first_name() + "'s Device"
        client = Client(name, random.choice([True, False]))
        client_list.append(client)

    # Print the client list
    print("All connected clients: ", end="\n\n")
    for client in client_list:
        print(client.name)
    print(end="\n\n")

    time.sleep(3)
    os.system('clear')

    print("All clients wanting to transmit: ", end="\n\n")
    for client in client_list:
        if client.status is True:
            print(client.name)
    print(end="\n\n")

    time.sleep(3)
    os.system('clear')


    contention_slots = contention(client_list)
    splitting(contention_slots)

    os.system('clear')
    printDTQ(DTQ)
    print("Contentions Resloved")
    print("Data transmission can now start according to the DTQ")
    while (not DTQ.empty()):
        client = DTQ.get()

        items = list(range(0, random.randint(1,50)))
        l = len(items)
        printProgressBar(0, l, prefix = client, suffix = 'Complete', length = 50)
        for i, item in enumerate(items):

            time.sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = client, suffix = 'Complete', length = 50)

    time.sleep(3)
    os.system('clear')

while(True):
    main()
