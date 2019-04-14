'''

Following code snippet implements Distributed Queuing

'''

import random, math, names, os, time, queue
start_time = time.time()

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
def printDTQ(dtq):
    print("DTQ: ")
    for client in list(dtq.queue):
        print(client, end=", ")
    print(end="\n\n")


def printCRQ(crq):
    print("CRQ: ")
    for client_list in list(crq.queue):
        if len(client_list) is not 0:
            for client in client_list:
                print(client.name, end=", ")
            print()
    print(end="\n\n")


def printContentionSlots(contention_slots):
    print("Contention Slots: ")
    for slot, clients in contention_slots.slots.items():
        print(slot, end=": ")
        for client in clients:
            print(client.name, end=", ")
        print()
    print(end="\n\n")

def printAllowedClients(client_list):
    print("Clients allowed to contend: ", end="\n\n")
    for client in client_list:
        if client.status is True:
            print(client.name, end=", ")
    print(end="\n\n")


def contention(client_list):

    '''
    This function initializes contention slots and asks the clients in client
    list to content for those slots randomly.
    '''

    # Printing clients allowed to contend
    printAllowedClients(client_list)

    # Initialize contention slots
    contention_slots = ContentionSlots()

    # Ask clients to randomly content for slots and append clients to their contented slot lists.
    for client in client_list:
        if client.status is True:
            contented_slot = random.randint(1, 5)
            contention_slots.slots[contented_slot].append(client)

    # Print the contention slots
    printContentionSlots(contention_slots)


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

    # Print the DTQ and CRQ
    printDTQ(DTQ)
    printCRQ(CRQ)

    if not CRQ.empty():
        resolution(CRQ)

    return None


def resolution(CRQ):

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

    print("All clients wanting to transmit: ", end="\n\n")
    for client in client_list:
        if client.status is True:
            print(client.name)
    print(end="\n\n")


    contention_slots = contention(client_list)
    splitting(contention_slots)

    print("Contentions Resloved")
    print("Time Taken: ", end="")
    print(time.time() - start_time, end="s\n")

main()
