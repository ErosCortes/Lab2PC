#commit inicial 
"""Script principal para generar, almacenar y ejecutar reportes."""
from generation.generation import gen_hosts, gen_logs, gen_maintenance
from storage.storage import create_db, insert_from_csv
import os

def run_all():
    print('Generando datos...')
    hosts = gen_hosts()
    logs = gen_logs(hosts)
    maint = gen_maintenance(hosts)

    os.makedirs('data', exist_ok=True)
    hosts.to_csv('data/hosts.csv', index=False)
    logs.to_csv('data/logs.csv', index=False)
    maint.to_csv('data/maintenance.csv', index=False)
    print('CSV generados en data/')

    print('Creando DB e insertando datos...')
    create_db()
    insert_from_csv()

    print('Ejecutando reportes Pandas (3.1)...')
    import reports.report_r31 as r31; r31.run()

    print('Generando gráficos (3.2)...')
    import reports.report_r32 as r32; r32.run()

    print('Ejecutando consultas SQL (3.3)...')
    import reports.report_r33 as r33; r33.run()

    print('\nTodo finalizado. Los archivos generados están en la carpeta data/ (CSV, DB y plots).')

if __name__ == '__main__':
    run_all()
