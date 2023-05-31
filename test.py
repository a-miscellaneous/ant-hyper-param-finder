import subprocess


def prep_command(comm, pd, mgs, mrc, pr):
    comm = comm.strip()
    comm = comm.split('"')
    part_2 = comm[2].strip().split(' ')
    comm.pop(2)
    for i in part_2:
        comm.append(i)

    command_copy = comm.copy()
    command_copy.append( str(pd))
    command_copy.append( str(mgs))
    command_copy.append( str(mrc))
    command_copy.append( str(pr))


    return command_copy

def black_box_function(pd, mgs, mrc, pr):
    com = prep_command(command, pd, mgs, mrc, pr)
    # print last 20 chars of the output
    for i in com: print(i)
    res = subprocess.run(com, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    res = res.split('\n')
    res = res[-4]
    score = 0
    try:
        score = float(res.split(' ')[-1][6:-2])
    except:
        score = 10

    return score


command = open("command.txt", "r").read()

if __name__ == "__main__":
    pd = 0.9708924196157915
    mgs = 56.9239059211837
    mrc = 0.03359814584366693
    pr = 0.1290747299750546


    print(black_box_function(pd, mgs, mrc, pr))