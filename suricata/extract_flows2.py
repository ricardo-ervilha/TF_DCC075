import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

window_size = timedelta(seconds=60)
buckets = {}  # chave -> dados acumulados

def follow(file):
    file.seek(0, 2)
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

def process_flow(event):
    flow = event.get("flow", {})
    features = {}
    features["Destination Port"] = event.get("dest_port")
    features["Total Fwd Packets"] = flow.get("pkts_toserver", 0)
    features["Total Backward Packets"] = flow.get("pkts_toclient", 0)
    features["Total Length of Fwd Packets"] = flow.get("bytes_toserver", 0)
    features["Total Length of Bwd Packets"] = flow.get("bytes_toclient", 0)
    features["Flow Duration"] = extractDuration(flow.get("start"), flow.get("end"))
    return features

def aggregate_and_emit(key, data, on_flow):
    duration = max(data["Flow Duration"] / 1_000_000, 0.001)
    total_packets = data["Total Fwd Packets"] + data["Total Backward Packets"]
    data["Flow Packets/s"] = total_packets / duration
    total_bytes = data["Total Length of Fwd Packets"] + data["Total Length of Bwd Packets"]
    data["Flow Bytes/s"] = total_bytes / duration
    if data["Total Length of Fwd Packets"] > 0:
        data["Down/Up Ratio"] = data["Total Length of Bwd Packets"] / data["Total Length of Fwd Packets"]
    else:
        data["Down/Up Ratio"] = 0
    on_flow(data)

def follow_flows(eve_log_path, on_flow):
    with open(eve_log_path, 'r') as f:
        for line in follow(f):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("event_type") != "flow":
                continue

            # chave = janela de tempo arredondada + IPs + porta destino
            ts = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            ts_window = ts.replace(microsecond=0)
            key = (ts_window, event.get("src_ip"), event.get("dest_ip"), event.get("dest_port"))

            new_data = process_flow(event)

            if key not in buckets:
                buckets[key] = new_data
            else:
                for k in ["Total Fwd Packets", "Total Backward Packets",
                          "Total Length of Fwd Packets", "Total Length of Bwd Packets"]:
                    buckets[key][k] += new_data[k]
                buckets[key]["Flow Duration"] = max(buckets[key]["Flow Duration"], new_data["Flow Duration"])
            
            #Emitir e limpar quando passar a janela
            expired_keys = [k for k in buckets if ts - k[0] >= window_size]
            for k in expired_keys:
                aggregate_and_emit(k, buckets[k], on_flow)
                del buckets[k]
