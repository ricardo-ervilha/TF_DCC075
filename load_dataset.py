import kagglehub
import pandas as pd
import os

def load():
    # Realiza o download do dataset (caso não tenha baixado), e o armazena em um .cache
    path = kagglehub.dataset_download("chethuhn/network-intrusion-dataset")
    # print(path) # Descomente caso queira ver onde foi guardado.

    filenames = [
        "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        "Friday-WorkingHours-Morning.pcap_ISCX.csv",
        "Monday-WorkingHours.pcap_ISCX.csv",
        "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
        "Tuesday-WorkingHours.pcap_ISCX.csv",
        "Wednesday-workingHours.pcap_ISCX.csv"
    ]