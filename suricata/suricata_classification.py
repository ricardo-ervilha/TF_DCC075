from extract_flows import follow_flows
import joblib

#Caminho onde é  salvo os logs do suricata
eve_log_path = '/var/log/suricata/eve.json'

randomForest = joblib.load("modelo/random_forest_model.joblib")
scaler = joblib.load("modelo/minmax_scaler.joblib")

#Testando
def meu_callback(flow_data):
    print(flow_data)

follow_flows(eve_log_path, meu_callback)