import subprocess
import numpy as np
import matplotlib.pyplot as plt
import rbfopt

import threading

command = open("command.txt", "r").read()
THREAD_AMOUNT = 6

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
def black_box_function(trial):
    mgs = trial.suggest_float('mgs', 2.0, 8.0)
    mrc = trial.suggest_float('mrc', 0.0, 0.1)
    pds = trial.suggest_float('pds', 0.0, 2.0)
    pdm = trial.suggest_float('pdm', 0.7, 1.0)
    prs = trial.suggest_float('prs', 0.0, 5.0)
    prm = trial.suggest_float('prm', 0.0, 1.0)
    ps = trial.suggest_float('ps', 0.0, 0.1)
    arg_array = [mgs, mrc, pds, pdm, prs, prm, ps]
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
    sum = 0
    for i in res:
        sum += i
    res = sum / len(res)

    return res


import optuna


if __name__ == "__main__":

    study = optuna.create_study(storage="sqlite:///db.sqlite3",  # Specify the storage URL here.
        study_name="all_params_02", direction="maximize", load_if_exists=True)
    # study.optimize(black_box_function, n_trials=1)
    cut_off = 50.0
    res = []
    lenngth = len(study.get_trials(deepcopy=True))
    print("LENGTH: ", lenngth)
    for i in study.get_trials(deepcopy=True):
        try:
            if float(i.values[0]) > cut_off:
                res.append(i)
        except:
            pass

    res = map(lambda x: {'score': x.values[0], 'params': x.params}, res)

    for i in res:
        print(i)


