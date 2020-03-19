'''
Author: Deepti Mahesh
Date: 31/10/2019

Undo Recovery
'''

import sys
import time
import random as rand
import os

disk, logs = dict(), list()

def roll_complete():
    complete = []
    global logs
    mod_logs = logs[::-1]
    for line in mod_logs:
        not_T = line.split()[0]
        if line[0] == 'T':
            string = line.replace(" ", "").split(',')
            if string[0] not in complete:
                disk[string[1]] = int(string[2])   #update based on if transaction in committed or not 
        elif not_T == 'COMMIT':
            complete.append(line.split()[1])

checkpoint_start,checkpoint_end = -1, -1
numof_line = 1

def case_three():
    '''
        End is present
    '''
    complete = []
    global logs
    mod_logs = (logs[checkpoint_start + 1:])[::-1]
    for line in mod_logs:
        not_T = line.split()[0]
        if line[0] == 'T':
            string = line.replace(" ", "").split(',')
            if string[0] not in complete:
                disk[string[1]] = int(string[2])
        elif not_T == 'COMMIT':
            complete.append(line.split(' ')[1])


def rollback():
    global checkpoint_start, checkpoint_end

    if checkpoint_end < checkpoint_start:
        checkpoint_end = -1

    if checkpoint_start == -1:
        if checkpoint_end == -1:
            roll_complete()
        else:
            print("Error with checkpoints found")
    else:
        if checkpoint_end == -1:
            case_two()
        else:
            case_three()


def case_two():
    '''
        Transaction not ended
    '''
    global logs, disk
    mod_logs = logs[checkpoint_start]
    mod_logs = mod_logs[mod_logs.find('(') + 1:mod_logs.find(')')]
    list_trans = mod_logs.replace(' ', '').split(",")
    complete = []
    for line in logs[::-1]:
        not_t = line.split(' ')[0]
        if len(list_trans) == 0:
            break
        else:
            if line[0] == 'T':
                string = line.replace(" ", "").split(',')
                if string[0] not in complete:
                    disk[string[1]] = int(string[2])
            elif not_t == 'COMMIT':
                complete.append(line.split(' ')[1])
            elif not_t == 'START':
                if (line.split())[1] != 'CKPT':
                    if line.split()[1] in list_trans:
                        list_trans.remove(line.split()[1])


def read_file(input_file):
    '''
        Parse given inputs
    '''
    global checkpoint_start, checkpoint_end, numof_line
    file = open(input_file)
    for line in file:
        if numof_line == 1:  # ie parse first line with init vals of variables
            variables = line.split()
            for i in range(len(variables)):
                if i % 2 != 0:
                    pass
                else:
                    disk[variables[i]] = int(variables[i + 1])
        else:
            inputs = line.strip()
            if inputs:
                logs.append(line[1:-2])
                if line.find('CKPT') != -1:
                    if line.find('START') != -1 or line.find('END') != -1:
                        checkpoint = numof_line - 3
                        if line.find('START') != -1:
                            checkpoint_start = checkpoint
                        if line.find('END') != -1:
                            checkpoint_end = checkpoint
        numof_line += 1
    


if __name__ == "__main__":
    # global logs
    input_file = sys.argv[1]
    output_file = open('20171212_2.txt', 'w')
    read_file(input_file)
    rollback()

    string, s_disk = '', sorted(disk)
    for i in sorted(disk):
        string += i + ' ' + str(disk[i]) + ' '
    output_file.write(string[:-1] + '\n')

    output_file.close()