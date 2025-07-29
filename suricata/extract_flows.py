import json
import pandas as pd
import time

#Caminho onde é  salvo os logs do suricata
eve_log_path = '/var/log/suricata/eve.json'

flow_data = []



def follow(file):
    file.seek(0,2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1) 
            continue
        yield line

def process_line(line):
    try:
        event = json.loads(line)
        if event.get("event_type") == "flow":
            flow = event.get("flow", {})
            return {
                "src_ip": event.get("src_ip"),
                "src_port": event.get("src_port"),
                "dest_ip": event.get("dest_ip"),
                "dest_port": event.get("dest_port"),
                "protocol": event.get("proto"),
                "pkts_toserver": flow.get("pkts_toserver"),
                "pkts_toclient": flow.get("pkts_toclient"),
                "bytes_toserver": flow.get("bytes_toserver"),
                "bytes_toclient": flow.get("bytes_toclient"),
                "start": flow.get("start"),
                "end": flow.get("end"),
                "age": flow.get("age"),
            }
    except json.JSONDecodeError:
        return None

with open(eve_log_path, 'r') as f:
    for line in follow(f):
        flow_data = process_line(line)
        if flow_data:
            print("Fluxo capturado: ", flow_data)  

