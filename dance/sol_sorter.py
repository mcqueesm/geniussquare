import json

with open('sols.json') as json_file:
    data = json.load(json_file)
    data = sorted(data['solutions'], key=lambda x: x[0])
    for x in data[0:10]:
        print(x)

    for x in data[-10:]:
        print(x) 