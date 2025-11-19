import pandas as pd

def cargar_hosts():
    df = pd.read_csv("../data/hosts.csv")

    print(df)

cargar_hosts()