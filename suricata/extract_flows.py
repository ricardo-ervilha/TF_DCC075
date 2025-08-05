import json
import pandas as pd
import time
from datetime import datetime


flow_data = []
datetime


def follow(file):
    file.seek(0,2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1) 
            continue
        yield line


def extractDuration(start, end):
    startDate = datetime.fromisoformat(start)
    endDate = datetime.fromisoformat(end)
    duration = endDate - startDate
    return duration.total_seconds() * 1_000_000

def process_line(line):
                #"src_ip": event.get("src_ip"),
                #"src_port": event.get("src_port"),
                #"dest_ip": event.get("dest_ip"),
                #"protocol": event.get("proto"),
                #"dest_port": event.get("dest_port"),
                #"total_fwd_packets": flow.get("pkts_toserver"),
                #"total_bwd_packets": flow.get("pkts_toclient"),
                #"flow_packets_per_sec": 
                #"total_fwd_bytes": flow.get("bytes_toserver"),
                #"total_bwd_bytes": flow.get("bytes_toclient"),
                #"duration": duration.microseconds
    try:
        event = json.loads(line)
        if event.get("event_type") == "flow":
            flow = event.get("flow", {})
            features = {}

            #dest_port     
            features["Destination Port"] = event.get("dest_port")

            #total_fwd_packets (pkts_toserver)   
            features["Total Fwd Packets"] = flow.get("pkts_toserver")

            #total_bwd_packets (pkts_toclient)
            features["Total Backward Packets"] = flow.get("pkts_toclient")

            
            #total_fwd_bytes (bytes_toserver)
            features["Total Length of Fwd Packets"] = flow.get("bytes_toserver")
            
            #total_bwd_bytes (bytes_toclient)
            features["Total Length of Bwd Packets"] = flow.get("bytes_toclient")


            #duration   (end - start)
            features["Flow Duration"] = extractDuration(flow.get("start"), flow.get("end"))
            
            
            duration = max(features["Flow Duration"] / 1000000, 0.001)
            #flow_packets_per_sec
            total_packets = features["Total Fwd Packets"] + features["Total Backward Packets"]
            features["Flow Packets/s"] = total_packets / duration

            #flow_bytes_per_sec 
            total_bytes = features["Total Length of Fwd Packets"] + features["Total Length of Bwd Packets"]
            features["Flow Bytes/s"] = total_bytes / duration
            
            #down_up_ratio
            features["Down/Up Ratio"] = features["Total Length of Bwd Packets"] / features["Total Length of Fwd Packets"]

           
            return features
        
    except json.JSONDecodeError:
        return None


def follow_flows(eve_log_path, on_flow):
    with open(eve_log_path, 'r') as f:
        for line in follow(f):
            flow_data = process_line(line)
            if flow_data:
                on_flow(flow_data)

