
import ast


BOUNDARY = 35.0
results = []
if __name__ == "__main__":
    with open("register_data.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linec = line.strip()
            linec = linec.split(":")[-1]
            linec = linec[:-3:1]
            linec = float(linec)

            if linec > BOUNDARY:
                params = line.split("{")
                params = params[2]
                params = params.replace("}", "").strip()[:-2]
                results.append(ast.literal_eval("{" + params + "}"))


    avg = {'mgs' : 0.0, 'mrc' : 0.0, 'pd' : 0.0, 'pr' : 0.0, 'target' : 0.0}
    max_target = {'mgs' : 0.0, 'mrc' : 0.0, 'pd' : 0.0, 'pr' : 0.0, 'target' : 0.0}

    for i in results:
        print(i)

    for i in results:
        if i['target'] > max_target['target']:
            max_target = i

    print("max_target",  max_target)


    for i in results:
        for key in i.keys():
            avg[key] += i[key]

    for key in avg.keys():
        avg[key] /= len(results)

    print(len(results))
    print(avg)
