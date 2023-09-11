import psycopg2
import os
import time
from concurrent.futures import ProcessPoolExecutor

def process_cal256(root_dir):
    subdirs_files_dict = {}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath == root_dir:
            continue
            
        subdir_name = os.path.basename(dirpath)
        file_list = filenames
        subdirs_files_dict[subdir_name] = file_list
    
    return subdirs_files_dict

def insert_into_db(k, im):
    conn = psycopg2.connect(
        host="localhost",
        database="",
        user="",
        password="",
        port=5432
    )
    cur = conn.cursor()
    path = f'{os.getcwd()}/256_ObjectCategories/{k}/{im}'
    insert_query = f'INSERT INTO image_table (v, location) VALUES (clip_image(\'{path}\'), \'{path}\');'
    cur.execute(insert_query)
    conn.commit()
    conn.close()

if __name__=='__main__':
    files = process_cal256('256_ObjectCategories')
    conn = psycopg2.connect(
        host="localhost",
        database="",
        user="",
        password="",
        port=5432
    )

    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS image_table (
            v REAL[],
            location VARCHAR,
            id SERIAL PRIMARY KEY
        );''')

    conn.commit()
    conn.close()

    abs_start = time.time()
    for i, k in enumerate(sorted(list(files.keys()))):
        start = time.time()
        
        def process(im):
            insert_into_db(k, im)

        with ProcessPoolExecutor(max_workers=16) as executor:
            executor.map(process, files[k])
        
        end = time.time()
        print(f'completed {k} in {end-start} second, {end-abs_start} elapsed so far')

