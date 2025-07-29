import json
import pandas as pd

#Caminho onde é  salvo os logs do suricata
eve_log_path = '/var/log/suricata/eve.json'

flow_data = []

with open(eve_log_path, 'r') as file:
    for line in file:
        try:
            event = json.loads(line)
            
            #Vamos filtrar pelos eventos do tipo Flow
            if event.get("event_type") == "flow":
                flow = event.get("flow", {})
                data = {
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
                flow_data.append(data)

        except json.JSONDecodeError:
            continue  


#Salva o resultado em um csv
df = pd.DataFrame(flow_data)
df.to_csv("suricata_flows.csv", index=False)
