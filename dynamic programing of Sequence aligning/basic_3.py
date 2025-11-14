#CSCI570

import sys
from resource import *
import time
import psutil

GAP_DELTA = 30
ALPHA = {'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94}, 'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48}, 'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110}, 'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}}


# string generation
def stringGen(base, index):
    s = base
    for i in index:
        copy = s
        s = s[0:i+1] + copy + s[i+1:]
    return s


# Basic Sequence Alignment Algorithm
def BasicAlign(X, Y):
    m = len(X)
    n = len(Y)
    DP_table = [[0 for _ in range(n+1)] for _ in range(m+1)]
    trace_table = [[0 for _ in range(n+1)] for _ in range(m+1)]
    for i in range(1, m+1):
        DP_table[i][0] = i*GAP_DELTA
        trace_table[i][0] = 'up'
    for j in range(1, n+1):
        DP_table[0][j] = j*GAP_DELTA
        trace_table[0][j] = 'left'
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            mismatch = ALPHA[X[i-1]][Y[j-1]]
            cost_diag = DP_table[i-1][j-1] + mismatch
            cost_up = DP_table[i-1][j] + GAP_DELTA
            cost_left = DP_table[i][j-1] + GAP_DELTA
            min_cost = min(cost_diag, cost_up, cost_left)
            DP_table[i][j] = min_cost

            if min_cost == cost_diag:
                trace_table[i][j] = 'diag'
            elif min_cost == cost_up:
                trace_table[i][j] = 'up'
            else:
                trace_table[i][j] = 'left'
    
    cost = DP_table[m][n]
    aligned_X = ""
    aligned_Y = ""
    i = m
    j = n
    
    while i > 0 or j > 0:
        dir = trace_table[i][j]
        if dir == 'diag':
            aligned_X = X[i-1] + aligned_X
            aligned_Y = Y[j-1] + aligned_Y
            i = i - 1
            j = j - 1
        elif dir == 'up':
            aligned_X = X[i-1] + aligned_X
            aligned_Y = '_' + aligned_Y
            i = i - 1
        else:
            aligned_X = '_' + aligned_X
            aligned_Y = Y[j-1] + aligned_Y
            j = j - 1
            
    return cost, aligned_X, aligned_Y

def read_input_file(filename):
    #read input.txt
    with open(filename, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    split_index = next(i for i in range(1, len(lines)) if lines[i].isalpha())
    
    string1 = lines[0]
    indices1 = [int(lines[i]) for i in range(1, split_index)]
    string2 = lines[split_index]
    indices2 = [int(lines[i]) for i in range(split_index + 1, len(lines))]
    
    return string1, indices1, string2, indices2 

def write_output_file(filename, cost, s1, s2, time, memory):
    with open(filename, "w") as file:
        file.write(str(cost) + "\n")
        file.write(s1 + "\n")
        file.write(s2 + "\n")
        file.write(str(time) + "\n")
        file.write(str(memory) + "\n")

def process_memory():
    #memory inspection func
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def main():
    #=========ARGUMENT==========
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    #=========START=============    
    start_time = time.time()        #time_capture. (precision?)
    memory_start = process_memory() #memory_inspection (CPU level)
    
    #=========INPUT DATA========
    base1, index1, base2, index2 =  read_input_file(input_file)
    s1 = stringGen(base1, index1)
    s2 = stringGen(base2, index2)
    
    #=========DP ALGO===========
    cost, aligned_X, aligned_Y = BasicAlign(s1, s2)
    
    #========ENDING============
    end_time = time.time()
    memory_end = process_memory()
    execution_time = (end_time - start_time)*1000
    total_memory_used = memory_end - memory_start
    
    #=======OUPUT DATA=========
    final_s1 = aligned_X
    final_s2 = aligned_Y
    write_output_file(output_file, cost, final_s1, final_s2, execution_time, total_memory_used)
    
main()
