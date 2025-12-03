"""Reportes con Pandas: respuestas a las preguntas de 3.1"""
import pandas as pd
import sqlite3
from config.config import DB_PATH

def run():
    conn = sqlite3.connect(DB_PATH)
    hosts = pd.read_sql_query('SELECT * FROM hosts;', conn)
    logs = pd.read_sql_query('SELECT * FROM logs;', conn)
    maint = pd.read_sql_query('SELECT * FROM maintenance;', conn)
    conn.close()

    
    c1 = hosts.groupby(['country', 'environment']).size().rename('count').reset_index()
    print('\n1) Servidores por país y entorno:\n', c1)

   
    pct_linux = (hosts['os'] == 'Linux').mean() * 100
    print(f'\n2) Porcentaje de servidores que usan Linux: {pct_linux:.2f}%')

   
    avg_resp = logs.groupby('id_host')['response_time_ms'].mean().rename('avg_resp').reset_index()
    merged = avg_resp.merge(hosts[['id', 'hostname']], left_on='id_host', right_on='id', how='left')
    print('\n3) Top 10 servidores por tiempo promedio de respuesta:\n', merged.sort_values('avg_resp', ascending=False).head(10))

   
    by_req = logs.groupby('request_type')['response_time_ms'].mean().rename('avg_resp').reset_index().sort_values('avg_resp', ascending=False)
    print('\n4) Tipo de request ordenado por tiempo medio (desc):\n', by_req)

  
    logs['failed'] = logs['status_code'] >= 400
    merged2 = logs.merge(hosts[['id', 'country']], left_on='id_host', right_on='id', how='left')
    pct_fail = merged2.groupby(['id_host', 'country'])['failed'].mean().rename('pct_failed').reset_index()
    print('\n5) Porcentaje de solicitudes fallidas por servidor y país (primeras 20 filas):\n', pct_fail.head(20))

   
    mtype = maint.groupby('type')['duration_min'].mean().rename('avg_duration').reset_index().sort_values('avg_duration', ascending=False)
    print('\n6) Tipo de mantenimiento más largo (promedio):\n', mtype)

    
    tech = maint['technician'].value_counts().rename_axis('technician').reset_index(name='count')
    print('\n7) Técnicos con más intervenciones (top 10):\n', tech.head(10))

   
    hours = maint.groupby('id_host')['duration_min'].sum().rename('total_min').reset_index()
    hours['hours'] = hours['total_min'] / 60.0
    print('\n8) Horas de mantenimiento por servidor (primeras 20 filas):\n', hours.head(20))

if __name__ == '__main__':
    run()
