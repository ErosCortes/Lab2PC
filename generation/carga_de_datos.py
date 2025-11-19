import pandas as pd


def cargar_hosts():
    df = pd.read_csv("hosts.csv")

    print(df)