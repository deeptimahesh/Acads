'''
Author: Deepti Mahesh
Date: 30/10/2019

Undo Logging 

Input:

Text file:
    Line 1 : Variables + values in disk
    Transaction i, Number of inst/actions
Round Robin Value x

Output:

Log records based on Round Robin value
'''

import sys
import time
import random as rand
import os

transactions = dict()
disk = dict()
memo = dict()

order = []

filename = sys.argv[1]
x = int(sys.argv[2])
output_file = open('20171212_1.txt', 'w')

def read_file(filename):
    '''
        Parse for variable names and transactions
    '''
    flag, t_num = False, None       # Check if first line or not
    for line in open(filename):
        if flag == False:
            variables = line.split()
            flag = True
            for i in range(len(variables)):
                if i % 2 == 0:
                    disk[variables[i]] = int(variables[i + 1])
        elif line.split(' ')[0][0] == 'T':
            t_num, lengths[t_num] = line.split()[0], int(line.split()[1])
            order.append(t_num)
            transactions[t_num] = []          # Initialize list of transactions
        elif line.find('(') == True or line.strip():
            transactions[t_num] += [line[:-1]]
        elif not line.strip():
            t_num = None
            
    for i in transactions.keys():
        t_completed[i] = False

def undo_logs(x):
    '''
        Iterate through the transactions
    '''
    i, start = 0, 0
    current = order[i]
    false_count = [1]
    while len(false_count) != 0:
        i += 1
        push_log(current, x, start)
        if i % len(transactions) == 0:
            start += x
            i = 0
        current, false_count = order[i], []
        for (_, val) in t_completed.items():
            if val == False:
                false_count.append(1)


temp_var_map = dict()
temp_var = dict()


lengths = dict()    # Lengths of transactions
t_completed = dict()

def push_log(current, x, start):
    if lengths[current] <= start:
        t_completed[current] = True
        return
    inst = (transactions[current])[start:start + x]

    if 0 == start:
        output_file.write('<START ' + current + '>' + '\n')
        print_mem()

    for line in inst:
        line = (line.strip()).replace(" ", "")
        if line.split('(')[0] == 'WRITE':
            var = line[line.find('(') + 1:line.find(',')]
            value = line[line.find(',') + 1:line.find(')')]
            output_file.write('<' + current + ', ' + var + ', '+ str(memo[var]) + '>' + '\n')
            memo[var] = int(temp_var[value])
            print_mem()

        elif line.split('(')[0] == 'READ':
            var = line[line.find('(') + 1:line.find(',')]
            value = line[line.find(',') + 1:line.find(')')]

            if var in temp_var_map.keys():
                temp_var[value] = memo[var]
                temp_var_map[var] = value
            else:
                temp_var_map[var] = value
                temp_var[value], memo[var] = disk[var], disk[var]
                
        elif line.split('(')[0] == 'OUTPUT':
            var = line[line.find('(') + 1:line.find(')')]
            disk[var] = memo[var]
        else:
            op = ''
            a = line[0:line.find(':')]
            if '+' in line:
                op = '+'
            elif '-' in line:
                op = '-'
            elif '*' in line:
                op = '*'
            elif '/' in line:
                op = '/'
            pos = line.find("=")
            b = line[pos + 1:line.find(op)]
            if op is '+':
                temp_var[a] = temp_var[b] + int(line[line.find(op) + 1:])
            if op is '-':
                temp_var[a] = temp_var[b] - int(line[line.find(op) + 1:])
            if op is '*':
                temp_var[a] = temp_var[b] * int(line[line.find(op) + 1:])
            if op is '/':
                temp_var[a] = float(temp_var[b]) + float(line[line.find(op) + 1:])
    condition = start + x
    if lengths[current] > condition:
        pass
    else:
        output_file.write('<COMMIT ' + current + '>' + '\n')
        print_mem()

def print_mem(flag = 0):
    temp_memo = sorted(memo)
    temp_disk = sorted(disk)
    memo_str = ''
    memo_disk = ''
    if flag == 0:
        for i in temp_memo:
            memo_str += i + ' ' + str(memo[i]) + ' '
        memo_str = memo_str[:-1]
        output_file.writelines(memo_str + '\n')
        flag = 1
    if flag == 1:
        memo_disk = ''
        for i in temp_disk:
            memo_disk += i + ' ' + str(disk[i]) + ' '
        memo_disk = memo_disk[:-1]
        output_file.write(memo_disk + '\n')

if __name__ == "__main__":
    filename = sys.argv[1]
    x = int(sys.argv[2])
    output_file = open('20171212_1.txt', 'w')
    read_file(filename)
    undo_logs(x)
    output_file.close()