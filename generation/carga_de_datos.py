import pandas as pd

def cargar_hosts(ruta):
    df = pd.read_csv(ruta)
    return df