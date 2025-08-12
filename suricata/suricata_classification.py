from extract_flows import follow_flows
import joblib
import numpy as np
import warnings
import sys 
warnings.filterwarnings("ignore")
#Caminho onde é  salvo os logs do suricata
eve_log_path = '/var/log/suricata/eve.json'

randomForest = joblib.load("modelo/random_forest_model.joblib")
scaler = joblib.load("modelo/minmax_scaler.joblib")

#Testando
def meu_callback(flow_data):
    flow_data_values  = np.array(list(flow_data.values())).reshape(1, -1)
    flow_data_scaled = scaler.transform(flow_data_values)
    predict = randomForest.predict(flow_data_scaled)
    if predict == 0:
        flow_data["Classification"] = "BENIGN"
    else:
        flow_data["Classification"] = "MALIGNANT"

    
    print(flow_data)
    print("\n")

def print_flow(flow_data):
    teste = flow_data

follow_flows(eve_log_path, meu_callback, test=sys.argv[1])
