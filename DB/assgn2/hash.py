'''
Created by Deepti Mahesh
5/10/2019

S: total records
bucket_index: initial hash function, ie modulo 2
new_index: new hash function (next one) initialized to modulo 4
bucket_count: initialized as 2

Main mem = 2
Buffer size = 20
'''
import sys
from random import random
import time as tik
import os

def insert_hash(num):
	'''
	Insert into buckets unless bucket > 75% full
	'''
	global S, count_total, repetitions

	hash_val = get_hash_val(num)
	flag, a = 1, 1
    #create bucket
	if hash_val not in buckets:
		buckets[hash_val] = [[]]

	for i in range(count_arr[hash_val]):
		if num not in buckets[hash_val][i]:
			flag = 0

	if a == 1:
		if flag == 0:
			lentemp = count_arr[hash_val]
			S += 1
			temp = lentemp - 1
			if len(buckets[hash_val][temp]) >= (5.0):
				temp, lentemp, count_total = temp + 1, lentemp + 1, \
					count_total + 1
				count_arr[hash_val] = lentemp
				# empty array append
				buckets[hash_val].append([])
			buckets[hash_val][temp].append(num)

			repetitions = append_rep(num)

	density = (S * 20.0) / count_total       
	if density >= (75.0*100)/100:
		make_new()

def append_rep(num):
	'''
	Append to_print
	'''
	global repetitions
	repetitions.append(num)
	if len(repetitions) >= (5.0):
		repetitions = print_result(repetitions)
	return repetitions

def get_hash_val(n, flag = 0):
    '''
    Compute Hash value to sort record into bucket
    '''
    if flag == 0:
        result = n % bucket_index
        if result < index:
            result = n % new_index
        return result
    else:
        return n % new_index

def print_result(buff):
    '''
    Prints result wanted
    '''
    for val in buff:
        print(val)
    buff = []
    return buff

def update_global():
	'''

	'''
	global index, bucket_index, new_index, bucket_count
	index = index + 1
	if bucket_count == new_index:
		bucket_index, new_index, index = bucket_index*2, bucket_index*2, 0

def to_replace():
	global count_total, count_arr
	global index
	arr, not_replace = [], []

	leny = count_arr[index]
	for i in range(leny):
		for value in buckets[index][i]:
			arr.append(value)

	count_total -= int(count_arr[index])
	not_replace.append(count_total)
	return arr

def make_new():
	'''
	Create new bucket
	'''
	global bucket_count, count_total
	global index, bucket_index, new_index

	bucket_count += 1
    
	replace_array = to_replace()
	buckets[index], count_arr[index], count_total = [[]], 1, count_total + 1

	buckets[bucket_count - 1] = [[]]
	count_arr[bucket_count - 1], count_total = 1, count_total + 1
	count_total += 1

	for value in replace_array:
		hash_val = get_hash_val(value, flag = 1)
		flag, a, b  = 1, 1, 3
		if hash_val not in buckets:
			buckets[hash_val] = [[]]
			count_arr[hash_val] = 1
			count_total += 1

		if a == 1:
			for j in range(count_arr[hash_val]):
				if value not in buckets[hash_val][j]:
					flag = 0

			if flag == 0:
				if a == 1:
					temp = count_arr[hash_val] - 1
				if b != 0:
					temp = count_arr[hash_val] - 1
					if len(buckets[hash_val][temp]) >= 5.0:
						count_arr[hash_val] += 1
						count_total, temp = count_total + 1, temp + 1
						buckets[hash_val].append([])
				buckets[hash_val][temp].append(value)
	update_global()

#Start of main
input_buffer, repetitions = [], []
S = 0
bucket_count = 2

#Initialize dictionary
buckets, count_arr = {}, {0: 1, 1: 1}
count_total = 2
index = 0
bucket_index, new_index = 2, 4
with open(sys.argv[1]) as filey:
    for line in filey:
        num = line.strip()
        input_buffer.append(int(num))
        if len(input_buffer) >= 5.0:
            for val in input_buffer:
                insert_hash(val)
            input_buffer = []

    for val in input_buffer:
        insert_hash(val)
    input_buffer = []

repetitions = print_result(repetitions)