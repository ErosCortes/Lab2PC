"""Reportes con Pandas y Matplotlib: gráficos solicitados."""
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
from config.config import DB_PATH

def run():
    conn = sqlite3.connect(DB_PATH)
    logs = pd.read_sql_query('SELECT * FROM logs;', conn, parse_dates=['timestamp'])
    maint = pd.read_sql_query('SELECT * FROM maintenance;', conn)
    hosts = pd.read_sql_query('SELECT * FROM hosts;', conn)
    conn.close()

    os.makedirs('data/plots', exist_ok=True)

 
    counts = hosts['country'].value_counts()
    plt.figure()
    counts.plot(kind='bar')
    plt.title('Servidores por país')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    plt.savefig('data/plots/servers_by_country.png')
    plt.close()
    print('Guardado: data/plots/servers_by_country.png')

    
    ts = logs['timestamp'].dt
    logs['hour_continuous'] = ts.hour + ts.minute / 60 + ts.second / 3600
    
    plt.figure(figsize=(10,5))
    plt.scatter(logs['hour_continuous'], logs['response_time_ms'], s=2, alpha=0.6) 
    plt.xlabel('Hora del día')
    plt.ylabel('Response time (ms)')
    plt.title('Hora del día vs Tiempo de respuesta')
    plt.xlim(0, 24) 
    plt.xticks(range(0, 25, 2)) 
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('data/plots/hour_vs_response.png')
    plt.close()
    print('Guardado: data/plots/hour_vs_response.png')

    
    notes_txt = ' '.join(maint['notes'].fillna('').astype(str).tolist())
    try:
        from wordcloud import WordCloud
        wc = WordCloud(width=800, height=400).generate(notes_txt)
        plt.figure(figsize=(10,5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('data/plots/wordcloud_notes.png')
        plt.close()
        print('Guardado: data/plots/wordcloud_notes.png')
    except Exception:
        with open('data/plots/notes_wordlist.txt', 'w', encoding='utf-8') as f:
            f.write(notes_txt)
        print('wordcloud no disponible, guardado data/plots/notes_wordlist.txt')

    
    merged = maint.merge(hosts[['id', 'country']], left_on='id_host', right_on='id', how='left')
    avg_maint = merged.groupby('country')['duration_min'].mean().rename('avg_maint').reset_index()
    logs2 = logs.merge(hosts[['id', 'country']], left_on='id_host', right_on='id', how='left')
    avg_resp = logs2.groupby('country')['response_time_ms'].mean().rename('avg_resp').reset_index()
    agg = avg_maint.merge(avg_resp, on='country', how='inner')
    plt.figure()
    plt.scatter(agg['avg_maint'], agg['avg_resp'])
    for i, row in agg.iterrows():
        plt.text(row['avg_maint'], row['avg_resp'], row['country'])
    plt.xlabel('Duración media mantención (min)')
    plt.ylabel('Tiempo medio respuesta (ms)')
    plt.title('Relación mantenimiento vs tiempo de respuesta por país')
    plt.tight_layout()
    plt.savefig('data/plots/maint_vs_resp_by_country.png')
    plt.close()
    print('Guardado: data/plots/maint_vs_resp_by_country.png')

    
    logs['month'] = pd.to_datetime(logs['timestamp']).dt.to_period('M')
    monthly = logs.groupby('month')['response_time_ms'].mean().reset_index()
    plt.figure(figsize=(8,4))
    monthly['response_time_ms'].plot()
    plt.xlabel('Mes')
    plt.ylabel('Tiempo medio de respuesta (ms)')
    plt.title('Tiempo de respuesta promedio por mes')
    plt.tight_layout()
    plt.savefig('data/plots/avg_response_by_month.png')
    plt.close()
    print('Guardado: data/plots/avg_response_by_month.png')

if __name__ == '__main__':
    run()
