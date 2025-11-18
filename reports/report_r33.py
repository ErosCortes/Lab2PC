"""Consultas SQL solicitadas en 3.3"""
import sqlite3
import pandas as pd
from config.config import DB_PATH

def run():
    conn = sqlite3.connect(DB_PATH)
    # 1. ¿Cuántos servidores hay por país y entorno?
    q1 = """SELECT country, environment, COUNT(*) as cnt FROM hosts GROUP BY country, environment;"""
    print('\n1) Servidores por país y entorno:\n', pd.read_sql_query(q1, conn))

    # 2. ¿Qué sistemas operativos predominan en Producción?
    q2 = """SELECT os, COUNT(*) as cnt FROM hosts WHERE environment='Production' GROUP BY os ORDER BY cnt DESC;"""
    print('\n2) OS predominantes en Production:\n', pd.read_sql_query(q2, conn))

    # 3. ¿Qué servidor tiene más mantenimientos registrados?
    q3 = """SELECT h.hostname, COUNT(m.id_maintenance) as cnt
            FROM maintenance m JOIN hosts h ON m.id_server=h.id
            GROUP BY m.id_server
            ORDER BY cnt DESC
            LIMIT 5;"""
    print('\n3) Servidores con más mantenimientos:\n', pd.read_sql_query(q3, conn))

    # 4. ¿Qué entornos (Production, Testing, Development) presentan más errores HTTP?
    q4 = """SELECT h.environment,
                   SUM(CASE WHEN l.status_code>=400 THEN 1 ELSE 0 END) as errors
            FROM logs l JOIN hosts h ON l.id_server=h.id
            GROUP BY h.environment
            ORDER BY errors DESC;"""
    print('\n4) Entornos con más errores HTTP:\n', pd.read_sql_query(q4, conn))

    # 5. ¿Qué técnico ha trabajado en más servidores de producción?
    q5 = """SELECT m.technician, COUNT(DISTINCT m.id_server) as servers
            FROM maintenance m JOIN hosts h ON m.id_server=h.id
            WHERE h.environment='Production'
            GROUP BY m.technician
            ORDER BY servers DESC
            LIMIT 10;"""
    print('\n5) Técnicos que han trabajado en más servidores de Production:\n', pd.read_sql_query(q5, conn))

    # 6. ¿Cuántas solicitudes totales maneja cada país por mes?
    q6 = """SELECT h.country, STRFTIME('%Y-%m', l.timestamp) as year_month, COUNT(*) as total_requests
            FROM logs l JOIN hosts h ON l.id_server=h.id
            GROUP BY h.country, year_month
            ORDER BY h.country, year_month;"""
    print('\n6) Solicitudes por país por mes (muestra primeras 20 filas):\n', pd.read_sql_query(q6, conn).head(20))

    conn.close()

if __name__ == '__main__':
    run()
