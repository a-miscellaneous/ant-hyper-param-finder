import subprocess
import numpy as np
import matplotlib.pyplot as plt
import rbfopt

import threading

command = open("command.txt", "r").read()
THREAD_AMOUNT = 6

SIM_SUM = 0

def prep_command(comm, arg_list):
    comm = comm.strip()
    comm = comm.split('"')
    part_2 = comm[2].strip().split(' ')
    comm.pop(2)
    for i in part_2:
        comm.append(i)

    command_copy = comm.copy()
    for i in arg_list:
        command_copy.append(str(i))
    return command_copy

def run_command(comm, result):
    res = subprocess.run(comm, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    res = res.split('\n')
    res = res[-4]
    score = 10
    try:
        score = float(res.split(' ')[-1][6:-2])
    except:
        pass

    result.append(score)

#bounds = [(0.0, 0.99000), (0.0, 100.0), (0.0, 0.150000), (0.0, 0.30000)]
def black_box_function():
    arg_array = []
    com = prep_command(command, arg_array)
    # print("STARTING")
    treads = []
    res = []
    for i in range(THREAD_AMOUNT):
        treads.append(threading.Thread(target=run_command, args=(com, res)))
    for i in treads:
        i.start()
    for i in treads:
        i.join()
    global SIM_SUM
    for i in res:
        SIM_SUM += i


    return res

if __name__ == "__main__":
    SIM_NUM = 1

    for i in range(SIM_NUM):
        black_box_function()

    runs = SIM_NUM * THREAD_AMOUNT

    print("Average score: " + str(SIM_SUM / runs))