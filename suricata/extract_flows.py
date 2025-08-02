import json
import pandas as pd
import time
from datetime import datetime
#Caminho onde é  salvo os logs do suricata
eve_log_path = '/var/log/suricata/eve.json'

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
            
            
            #flow_packets_per_sec
            total_packets = features["Total Fwd Packets"] + features["Total Backward Packets"]

            duration = max(features["Flow Duration"], 0.001)
            features["Flow Packets/s"] =  (total_packets / (duration / 1000000))

            #flow_bytes_per_sec 
            total_bytes = features["Total Length of Fwd Packets"] + features["Total Length of Bwd Packets"]
            features["Flow Bytes/s"] = total_bytes / (duration / 1000000)
            
            #down_up_ratio
            features["Down/Up Ratio"] = features["Total Length of Bwd Packets"] / features["Total Length of Fwd Packets"]

            return features
        
    except json.JSONDecodeError:
        return None

with open(eve_log_path, 'r') as f:
    for line in follow(f):
        flow_data = process_line(line)
        if flow_data:
            print("Fluxo capturado: ", flow_data)  

