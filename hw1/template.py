# Networking Homework 1
# Sam Eakin
# 2/12/2018

import csv

class Packet:
    """
    This class models a packet
    """
    def __init__(self, id, destination, propD, transD):
        self.id = id #sequence number
        self.destination = destination
        self.release_time = 0
        self.head_of_q = 0 
        self.end_of_transmission = 0
        self.reception = 0
        self.end_to_end = 0
        self.queueing_delay = 0
        self.prop_delay = propD
        self.trans_delay = transD
    def __str__(self):
        return 'P[%d]' % self.id


class Event:
    """
    The base class for events
    """
    def __init__(self, node, time, pkt, tag=''):
        self.node = node
        self.time = time
        self.pkt = pkt
        self.tag = tag

    def __str__(self):
        return '%s %s %d %s' % (self.tag, str(self.node), self.time, str(self.pkt))


class Enqueue(Event):
    """
    This event indicates that a packet was enqueued
    """
    def __init__(self, node, time, pkt):
        Event.__init__(self, node, time, pkt, tag='enqueue')


class StartTransmission(Event):
    """
    This event indicates the start of a packet transmission
    """
    def __init__(self, node, time, pkt):
        Event.__init__(self, node, time, pkt, tag='start-tx')


class EndTransmission(Event):
    """
    This event indicates the completion of a packet transmission
    """
    def __init__(self, node, time, pkt):
        Event.__init__(self, node, time, pkt, tag='end-tx')


class EndReception(Event):
    """
    This event indicates the completion of a packet reception
    """
    def __init__(self, node, time, pkt):
        Event.__init__(self, node, time, pkt, tag='recv')


class Node:
    def __init__(self, name):
        self.name = name
        self.queue = [] # packets waiting to be transmitted

    # Add packet to queue, then start transmitting first packet in queue
    def enqueue(self, sim, pkt):
        pkt.release_time = sim.current_time
        if len(self.queue) == 0:
             sim.schedule(StartTransmission(self, sim.current_time, pkt)) # start sending first item in queue 
             pkt.head_of_q = sim.current_time    
        self.queue.append(pkt)
       
    # Remove packet from queue, End transmission for that packet
    def start_transmission(self, sim, pkt):
        assert(self.queue[0] == pkt)
        self.queue = self.queue[1:]
        sim.schedule(EndTransmission(self, sim.current_time + sim.transmission_delay, pkt))
        pkt.queueing_delay = sim.current_time - pkt.release_time
        if len(self.queue) > 0:
            nextpkt = self.queue[0]
            nextpkt.head_of_q = sim.current_time

    # Packet is done transmitting, Start transmitting the next packet in queue
    def end_transmission(self, sim, pkt):
        sim.schedule(EndReception(pkt.destination, 
            sim.current_time + sim.prop_delay, 
            pkt))
        pkt.end_of_transmission = sim.current_time
        if len(self.queue) > 0:
            sim.schedule(StartTransmission(self, sim.current_time, self.queue[0]))

    # Packet has reached it's destination
    def receive(self, sim, pkt):
        pkt.reception = sim.current_time 
        pkt.end_to_end = sim.current_time - pkt.release_time

    def __str__(self):
        return '%s' % self.name


class Simulator:
    def __init__(self, prop_delay, transmission_delay):
        self.prop_delay = prop_delay
        self.transmission_delay = transmission_delay
        self.queue = []
        self.current_time = 0

    def schedule(self, event):
        self.queue.append(event)

    def run(self):
        with open('sim.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['Seq', 'Release', 'HOQ', 'End of Trans', 
                             'Reception', 'End-to-End','Queueing',
                              'Prop','Transmission'])

            print('%10s %5s %20s %10s' % ('time', 'node', 'event', 'pkt'))
            while len(self.queue) != 0:
                self.queue = sorted(self.queue, key=lambda x: x.time)
                event = self.queue[0]
                self.current_time = event.time
                self.queue = self.queue[1:]

                
                print('%10d %5s %20s %10s' % (self.current_time, event.node, event.tag, event.pkt))

                if isinstance(event, Enqueue):
                    event.node.enqueue(sim, event.pkt)
                elif isinstance(event, StartTransmission):
                    event.node.start_transmission(sim, event.pkt)
                elif isinstance(event, EndTransmission):
                    event.node.end_transmission(sim, event.pkt)
                elif isinstance(event, EndReception):
                    event.node.receive(sim, event.pkt)
                    writer.writerow([event.pkt.id, 
                        event.pkt.release_time, 
                        event.pkt.head_of_q, 
                        event.pkt.end_of_transmission,
                        event.pkt.reception, 
                        event.pkt.end_to_end, 
                        event.pkt.queueing_delay, 
                        event.pkt. prop_delay, 
                        event.pkt.trans_delay
                        ])
                else:
                    raise Exception("unknown event")

if __name__ == "__main__":
    propD = 1
    transD = 10
    sim = Simulator(propD, transD)
    node_a = Node('A')
    node_b = Node('B')

    time = 0
    maxTime = 10000
    packetID = 0

    # Release 10 packets every 1000 ticks
    while time < maxTime:
        for p in range(0,10):
            sim.schedule(Enqueue(node_a, time, Packet(packetID, node_b, propD, transD))) # Event(Node, time, Packet)
            packetID += 1
        time += 1000

    sim.run()

