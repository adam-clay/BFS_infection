import matplotlib.pyplot as plt
import outbreak
import pathlib
import os
import numpy as np

def plot_num_nodes_vs_day_infected(all_days, plt_name, p_count):
    all_days_int = all_days

    all_days_int = \
        [[d for d in trial if d != float("inf")] \
            for trial in all_days]

    for trial in all_days_int:
        for n in range(len(trial)):
            trial[n] = int(round(trial[n]))

    for n in range(2):
        curr_days = all_days_int[n]
        plt.hist(curr_days, bins = range(max(curr_days)), \
            alpha = 0.5, \
            label = 'p = ' + str("{:.1f}".format(p_count)))

        p_count += .2

    plt.legend(loc = 'upper right', bbox_to_anchor=(1, 0.6), \
        prop={'size': 6})

    plt.xlabel("Day Infected")
    plt.ylabel("Number of Nodes")
    
    plt.savefig(plt_name)
    plt.clf()



def plot_probs_vs_nodes(all_probs, plt_name):
    p_count = .1

    for n in range(4):
        curr_probs = all_probs[n]
        plt.plot(range(len(curr_probs)), curr_probs, \
            label = 'p = ' + str("{:.1f}".format(p_count)))

        p_count += .2

    plt.legend(loc = 'upper right', bbox_to_anchor=(1, 0.6), \
        prop={'size': 6})

    plt.xlabel("Nodes")
    plt.ylabel("Probability of Infection")
    
    plt.savefig(plt_name)
    plt.clf()



def analyze_dir(directory, plt_name1, plt_name2 = None):
    all_probs = [[]] * 4
    all_days = [[]] * 4
    f_count = 0
    
    f_list = pathlib.Path(pathlib.Path().absolute() / directory)\
        .rglob("*.txt")

    for f in f_list:
        all_probs[f_count], all_days[f_count] = \
            read_file_to_lists(f)

        f_count += 1
    
    #plot_probs_vs_nodes(all_probs, plt_name1)
    #plot_num_nodes_vs_day_infected(all_days[:2], plt_name1, 0.1)
    #plot_num_nodes_vs_day_infected(all_days[2:], plt_name2, 0.5)

    return all_probs, all_days

        

def analyze_outbreak(filename):
    #prob_infect, avg_day = read_file_to_lists(filename)

    """
    nodes_infected = count_nodes_infected(prob_infect)

    
    print("Nodes infected for " + str(filename) + \
        " = " + str(nodes_infected))
    """

    return read_file_to_lists(filename)

def read_file_to_lists(filename):
    prob_infect = []
    avg_day = []

    with open(filename) as file_in:
        empty_line = False

        for line in file_in:
            if len(line.strip()) == 0 :
                empty_line = True
            if empty_line == False:
                prob_infect.append(float(line.rstrip()))
            else:
                try:
                    avg_day.append(float(line.rstrip()))
                except:
                    avg_day.append(line.rstrip())
    
    return prob_infect, avg_day[1:]

def count_nodes_infected(prob_infect):
    count = 0

    for n in prob_infect:
        if n != float(0):
            count += 1

    return count

def get_prob_ratio(dir1, dir2, plt_name):
    dir1_probs, dir1_days = analyze_dir(dir1, plt_name, plt_name)
    dir2_probs, dir1_days = analyze_dir(dir1, plt_name, plt_name)

    print(dir1_probs)
    print(dir2_probs)
    ratio = dir1_probs

    for n in range(len(dir1_probs)):
        for i in range(len(dir1_probs[0])):
            if dir2_probs[n][i] != 0:
                ratio[n][i] /= dir2_probs[n][i]
            else:
                ratio[n][i] = 0

    plot_probs_vs_nodes(ratio, plt_name)

