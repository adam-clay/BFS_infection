import sys
import random
import queue


############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [line.split(',') for line in f.read().splitlines()]

    N = int(raw[0][0])
    sin = raw[1]
    s = []
    for st in sin:
        s.append(int(st))
    adj_list = []
    for line in raw[2:]:
        if line == ['-']:
            adj_list.append([])
        else:
            adj_list.append([int(index) for index in line])
    return N, s, adj_list

def writeOutput(output_file, prob_infect, avg_day):
    with open(output_file, 'w') as f:
        for i in prob_infect:
            f.write(str(i) + '\n')
        f.write('\n')
        for i in avg_day:
            f.write(str(i) + '\n')

 

def Run(input_file, output_file):
    N, s, adj_list = readGraph(input_file)
    prob_infect, avg_day =   model_outbreak(N, s, adj_list)
    writeOutput(output_file, prob_infect, avg_day)



def  BFS(N, s, adj_list):
    level = ['x'] * N
    #######################################

    # COPY YOUR BFS CODE FROM PART 1 HERE

    ########################################
    to_visit = queue.Queue(maxsize = N)
    to_visit.put(s)
    
    visited = [False] * N
    visited[s] = True

    level[s] = 0

    while not to_visit.empty():
        curr = to_visit.get()

        for adj in adj_list[curr]:
            if visited[adj] != True:
                visited[adj] = True
                level[adj] = level[curr] + 1
                to_visit.put(adj)

    return level

#######################################

# WRITE YOUR SOLUTION IN THIS FUNCTION

########################################

"""
so, this is going to run through the graph n and return a list
of bools size = N, infected[i] will be true if node i becomes
infected, and false if node i is not infected

it will also return the set of days in which it was infected,
a node cannot be infected twice, so I will only add a node to
the queue to_infect once and record the day it was first infected

day is a list of integers giving the day of which the node was
infected, or the string 'inf' if the node was never infected
"""
def random_outbreak(N, sources, adj_list, p):
    infected = [False] * N 

    day = ['inf'] * N

    to_infect = queue.Queue(maxsize = N)

    for s in sources:
        to_infect.put(s)
        infected[s] = True
        day[s] = 0
    
    while not to_infect.empty():
        curr = to_infect.get()

        for adj in adj_list[curr]:
            r = random.uniform(0,1)

            if (infected[adj] != True) and (r <= p):
                infected[adj] = True
                day[adj] = day[curr] + 1
                to_infect.put(adj)
    
    return infected, day


def trials(N, sources, adj_list, prob_infect, avg_day, p):
    days_infected = [0] * N

    for i in range(100):
        infected, day = random_outbreak(N, sources, adj_list, p)
        
        for n in range(len(infected)):
            if infected[n] == True:
                prob_infect[n] += 1
                days_infected[n] += 1

                if avg_day[n] == 'inf':
                    avg_day[n] = day[n]
                else:
                    avg_day[n] += day[n]

    # if days_infected[n] == 0 then prob_infect[n] ==  0, and 
    # avg_day[n] == 'inf' which is the desired output:
    # only computing the average over days the node was infected
    for n in range(len(avg_day)):
        if days_infected[n] != 0:
            avg_day[n] /= days_infected[n]
            prob_infect[n] /= 100
    
    return prob_infect, avg_day


def model_outbreak(N, s, adj_list):
    # Again, you are given N, s, and the adj_list
    # You can also call your BFS algorithm in this function,
    # or write other functions to use here.
    # Return two lists of size n, where each entry represents one vertex:
    prob_infect = [0]*N
    # the probability that each node gets infected after a run of the experiment
    avg_day = ['inf']*N
    # the average day of infection for each node
    # (you can write 'inf' for infinity if the node is never infected)
    # The code will write this information to a single text file.
    # If you do not name this file at the command prompt, it will be called 'outbreak_output.txt'.
    # The first N lines of the file will have the probability infected for each node.
    # Then there will be a single space.
    # Then the following N lines will have the avg_day_infected for each node.
    p = [0.1, 0.3, 0.5, 0.7]

    prob_infect, avg_day = \
        trials(N, s, adj_list, prob_infect, avg_day, p[3])

    return prob_infect, avg_day

############################

# DO NOT CHANGE THIS PART!!

############################


# read command line arguments and then run
def main(args=[]):
    filenames = []

    #graph file
    if len(args)>0:
        filenames.append(args[0])
        input_file = filenames[0]
    else:
        print()
        print('ERROR: Please enter file names on the command line:')
        print('>> python outbreak.py graph_file.txt output_file.txt')
        print()
        return

    # output file
    if len(args)>1:
        filenames.append(args[1])
    else:
        filenames.append('outbreak_output.txt')
    output_file = filenames[1]

    Run(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])    
