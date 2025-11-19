#commit inicial 
"""Script principal para generar, almacenar y ejecutar reportes."""
from generation.generation import gen_logs, gen_maintenance
from storage.storage import create_db, insert_from_csv
import os
from generation.carga_de_datos import cargar_hosts
def run_all():
    print('Generando datos...')

    #carga los datos desde el csv otorgado como dataset
    hosts = cargar_hosts("data/hosts.csv")
    print(hosts)
    

    #crea los logs en base a los hosts para mantener coherencia
    logs = gen_logs(hosts)
    print(logs)

    #crea los mantenimientos en base a los hosts para mantener coherencia
    maint = gen_maintenance(hosts)
    print(maint)

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
