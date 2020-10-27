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

print(len(data))

data_dedup = list(dict.fromkeys(data))

print(len(data_dedup))


@dataclass
class fastq_file:
    case: str
    samplelbl: str
    sample: str
    datatype: str
    lanes: object


@dataclass
class lane:
    path: str
    lane: int
    marker_forward: str
    marker_reverse: str
    barcode: str


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
    load_data = fastq_file(case, samplelbl, sample, datatype, lane_data)

    opjson = jsons.dump(load_data)
    print(opjson)
