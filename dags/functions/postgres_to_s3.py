from airflow.providers.postgres.hooks.postgres import PostgresHook
from tempfile import NamedTemporaryFile
import csv
from airflow.utils.db import provide_session
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tempfile import NamedTemporaryFile
import logging

def _postgres_to_s3(ds):
    #https://www.youtube.com/watch?v=rcG4WNwi900
    #first query data from psql and save in text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('select * from games;')
    with NamedTemporaryFile(mode='w') as f: #puts file in temp folder
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info(f'Saved postgres data in text file: games.txt')
    #step 2: upload text file into s3
        s3_hook = S3Hook(aws_conn_id='aws_hook')
        s3_hook.load_file(
            filename=f.name,
            key=f'games/games_{ds}.csv',
            bucket_name='mlb-project',
            replace=True
        )
        logging.info(f' {f.name} has been pushed to S3')