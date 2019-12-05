#!/bin/python
import re
from decimal import Decimal

with open('test.out','r') as details:
    transaction = dict()
    omschrijving = list()
    current_transaction = 0

    for line in details:
        line_list = [x for x in line.split()] 
        if len(line_list) > 0:
            if re.match("[0-9][0-9]\-[0-9][0-9]\-[0-9][0-9][0-9][0-9]",''.join(line_list[0])):
                current_transaction += 1
                transaction[current_transaction] = dict()
                transaction[current_transaction]['date'] = line_list[0]
                transaction[current_transaction]['value'] = ''.join(line_list[-1:])
                transaction[current_transaction]['omschrijving'] = []
                transaction[current_transaction]['omschrijving'].append(''.join(line_list[2:-1]))
        
            else :
                transaction[current_transaction]['omschrijving'].append(''.join(line_list))
                #print(transaction[current_transaction]['omschrijving'])
#                print(''.join(line_list))

unsorted_keys = []
for k in transaction:
    unsorted_keys.append([k, transaction[k]['value']])

sorted_keys = sorted(unsorted_keys, key= lambda x: Decimal(re.sub("[^\d.]",'',x[1])))

for key in sorted_keys:
    print(transaction[key[0]])
