import time
import random
import json
import subprocess

from bayes_opt import BayesianOptimization
from bayes_opt.util import UtilityFunction, Colours

import asyncio
import threading

try:
    import json
    import tornado.ioloop
    import tornado.httpserver
    from tornado.web import RequestHandler
    import requests
except ImportError:
    raise ImportError(
        "In order to run this example you must have the libraries: " +
        "`tornado` and `requests` installed."
    )


TRIES_PER_OPTIMIZER = 100



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

    # for i in command_copy: print(i)
    return command_copy

def black_box_function(pd, mgs, mrc, pr):
    com = prep_command(command, pd, mgs, mrc, pr)
    # print last 20 chars of the output
    print(com[-4], com[-3], com[-2], com[-1])
    res = subprocess.run(com, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    res = res.split('\n')
    res = res[-4]
    score = 0
    try:
        score = float(res.split(' ')[-1][6:-2])
    except:
        score = 10

    return score




class BayesianOptimizationHandler(RequestHandler):
    """Basic functionality for NLP handlers."""
    _bo = BayesianOptimization(
        f=black_box_function,
        pbounds={"pd": (0.5, 1.0), "mgs": (0, 80), "mrc": (0.0, 0.2), "pr": (0.05, 0.3)}
    )
    _uf = UtilityFunction(kind="ucb", kappa=3, xi=1)

    def post(self):
        """Deal with incoming requests."""
        body = tornado.escape.json_decode(self.request.body)

        try:
            self._bo.register(
                params=body["params"],
                target=body["target"],
            )
            print("BO has registered: {} points.".format(len(self._bo.space)), end="\n\n")
        except KeyError:
            pass
        finally:
            suggested_params = self._bo.suggest(self._uf)

        self.write(json.dumps(suggested_params))


def run_optimization_app():
    asyncio.set_event_loop(asyncio.new_event_loop())
    handlers = [
        (r"/bayesian_optimization", BayesianOptimizationHandler),
    ]
    server = tornado.httpserver.HTTPServer(
        tornado.web.Application(handlers)
    )
    server.listen(9009)
    tornado.ioloop.IOLoop.instance().start()

file = open("register_data.txt", "w+")
def run_optimizer():
    global optimizers_config
    config = optimizers_config.pop()
    name = config["name"]
    colour = config["colour"]

    register_data = {}
    max_target = None
    for _ in range(TRIES_PER_OPTIMIZER):
        status = name + " wants to register: {}.\n".format(register_data)

        resp = requests.post(
            url="http://localhost:9009/bayesian_optimization",
            json=register_data,
        ).json()
        target = black_box_function(**resp)

        register_data = {
            "params": resp,
            "target": target,
        }

        if max_target is None or target > max_target:
            max_target = target

        status += name + " got {} as target.\n".format(target)
        status += name + " will to register next: {}.\n".format(register_data)
        # save register_data to file
        print("t: {}.\n".format(register_data))
        file.write(" will to register next: {}.\n".format(register_data))
        print(colour(status), end="\n")

    global results
    results.append((name, max_target))
    print(colour(name + " is done!"), end="\n\n")


command = open("command.txt", "r").read()

if __name__ == "__main__":
    with open("command.txt", "r") as f:
        command = f.read()


    ioloop = tornado.ioloop.IOLoop.instance()
    optimizers_config = [
        {"name": "optimizer 1", "colour": Colours.red},
        {"name": "optimizer 2", "colour": Colours.green},
        {"name": "optimizer 3", "colour": Colours.blue},
        {"name": "optimizer 4", "colour": Colours.cyan},
        {"name": "optimizer 5", "colour": Colours.purple},
        {"name": "optimizer 6", "colour": Colours.yellow},
        {"name": "optimizer 7", "colour": Colours.green},
        {"name": "optimizer 8", "colour": Colours.yellow},
        {"name": "optimizer 9", "colour": Colours.blue},
        {"name": "optimizer 10", "colour": Colours.red},
    ]

    app_thread = threading.Thread(target=run_optimization_app)
    app_thread.daemon = True
    app_thread.start()

    targets = (
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer,
        run_optimizer
    )
    optimizer_threads = []
    for target in targets:
        optimizer_threads.append(threading.Thread(target=target))
        optimizer_threads[-1].daemon = True
        optimizer_threads[-1].start()

    results = []
    for optimizer_thread in optimizer_threads:
        optimizer_thread.join()

    for result in results:
        print(result[0], "found a maximum value of: {}".format(result[1]))

    ioloop.stop()
    file.close()