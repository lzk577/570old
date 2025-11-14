import time
import sys
from resource import *
import psutil

GAP_DELTA = 30
ALPHA = {'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94}, 'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48}, 'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110}, 'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}}

#From basic_3.py
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
#End of Basic Alignment


def align_cost(X, Y):   #X - First string, Y - Second string
    m = len(X)
    n = len(Y)
    prev = [j*GAP_DELTA for j in range(n+1)]    #Initialize first row
    for i in range(1, m+1):
        curr = [i*GAP_DELTA] + [0]*n    #Initialize second row
        for j in range(1, n+1):
            diag_cost = prev[j-1] + ALPHA[X[i-1]][Y[j-1]]   #Both are aligned
            up_cost = prev[j] + GAP_DELTA   #Y is not aligned
            right_cost = curr[j-1] + GAP_DELTA  #X is not aligned
            curr[j] = min(diag_cost, up_cost, right_cost)
        prev = curr
    return prev
    
def find_alignment(X, Y):
    m = len(X)
    n = len(Y)
    aligned_X = ""
    aligned_Y = ""
    if m==0:    #Blank X
        return n*GAP_DELTA, '_'*n, Y
    elif n==0:   #Blank Y
        return m*GAP_DELTA, X, '_'*m
    elif m==1 or n==1:   #Basic algorithm
        return BasicAlign(X, Y)
    #Normal case
    mid_X = m//2
    score_left = align_cost(X[:mid_X], Y)
    score_right = align_cost(X[mid_X:][::-1],Y[::-1])
    min_cost = None
    for j in range(n+1):
        c = score_left[j] + score_right[n-j]
        if min_cost is None or c<min_cost:
            min_cost = c
            k = j
    cost_left, str_left_1, str_left_2 = find_alignment(X[:mid_X],Y[:k])
    cost_right, str_right_1, str_right_2 = find_alignment(X[mid_X:],Y[k:])
    return cost_left+cost_right, str_left_1+str_right_1, str_left_2+str_right_2            

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

def get_memory_kb():
    #memory inspection func
    return resource.getrusage(resource.RSUAGE_SELF).ru_maxrss

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
    base1, index1, base2, index2 = read_input_file(input_file)
    s1 = stringGen(base1, index1)
    s2 = stringGen(base2, index2)
    
    #=========DP ALGO===========
    cost, final_s1, final_s2 = find_alignment(s1, s2)
    
    #========ENDING============
    end_time = time.time()
    memory_end = process_memory()
    execution_time = (end_time - start_time)*1000
    total_memory_used = memory_end - memory_start
    
    #=======OUPUT DATA=========
    #cost = 1
    #final_s1 = s1
    #final_s2 = s2
    write_output_file(output_file, cost, final_s1, final_s2, execution_time, total_memory_used)
    
    
main()
