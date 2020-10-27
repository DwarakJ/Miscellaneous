import jsons
import json
import datetime
import time
from dataclasses import dataclass
import re

file_path_json = "./filetree-sample-data.json"

with open(file_path_json) as f:
    data = json.load(f)

data.sort()

data_dedup = list(dict.fromkeys(data))


@dataclass
class fastq_file:
    case: str
    samplelbl: str
    sample: str
    datatype: str
    lanes: list


@dataclass
class lane:
    path: str
    lane: int
    marker_forward: str
    marker_reverse: str
    barcode: str


w = open("final.json", 'w', encoding='utf-8')
opjson = {}
for each_file in data:
    path_ip = re.split('_|-|/', each_file)
    case = path_ip[0]
    samplelbl = path_ip[1]
    sample = case+'-'+samplelbl
    datatype = path_ip[2]
    barcode = path_ip[3]
    marker_forward = path_ip[7]
    marker_reverse = path_ip[8]
    lane_num = int(re.findall('[1-9]', path_ip[9])[0])
    lane_data = lane(each_file, lane_num, marker_forward,
                     marker_reverse, barcode)
    load_data = fastq_file(case, samplelbl, sample, datatype, [])

    # print(load_data, lane_data)

    opjson = jsons.dump(load_data, sort_keys=False)
    if opjson[samplelbl] is not samplelbl:
        opjson["lanes"].append(jsons.dump(lane_data), sort_keys=False)

# opjson[case]["lanes"][]

# print(opjson)

# print(opjson)
w.write(json.dumps(opjson, sort_keys=False, indent=4))
