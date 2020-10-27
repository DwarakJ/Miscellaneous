import argparse
from dataclasses import dataclass
import re
import jsons
import json

@dataclass
class fastq:
    case_id: str
    sample_label: str
    sample_id: str
    data_type: str
    lanes: list


@dataclass
class lane:
    path: str
    lane: int
    marker_forward: str
    marker_reverse: str
    barcode: str

def extract_data(input):
    metadata = {}

    for file in input:

        # Splitting the sentense by _ , - and /
        raw = re.split('_|-|/', file)

        fastq = jsons.dump(_get_fastq_data(raw))
        lanes = jsons.dump(_get_lane_data(file,raw))

        # Loading the fastq and lane data into output json
        metadata = load_data(fastq, lanes, metadata)
    
    return metadata

def _get_fastq_data(raw):
    # fastq file
    case = raw[0]
    samplelbl = raw[1]
    sample = raw[0]+'-'+raw[1]
    datatype = raw[2]

    fastq_temp = fastq(case, samplelbl, sample, datatype, [])

    return fastq_temp

def _get_lane_data(file,raw):
    # Lanes
    lane_num = int(re.findall('[1-9]', raw[9])[0])
    marker_forward = raw[7]
    marker_reverse = raw[8]
    barcode = raw[3]

    lane_temp = lane(file, lane_num, marker_forward, marker_reverse, barcode)

    return lane_temp


def load_data(fastq, lanes, output):

    if fastq["case_id"] not in output:
        output[fastq["case_id"]] = {}
        output[fastq["case_id"]]=jsons.dump(fastq)

    output[fastq["case_id"]]["lanes"].append(jsons.dump(lanes))
    
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FileTree Metadata Extraction")

    try:
        parser.add_argument('--source_file_name', help='fastq file', required=True)
        parser.add_argument('--destination_file_name', help='extracted json file', required=True)

        args = parser.parse_args()

        with open(args.source_file_name) as f:
            data = json.load(f)

        result = extract_data(data)

        t = []
        z = {}
        for k in result:
            #print(result[k])
            temp = str(result[k]).strip("\n").replace("\\",'')
            t.append(json.dumps(temp, indent=4))

        z["data"] = t

        with open("result2.json", 'w+', encoding="utf-8") as f:
            f.write(json.dumps(z, indent=4))


    except Exception as e:
        print(e)
