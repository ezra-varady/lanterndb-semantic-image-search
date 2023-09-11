import psycopg2
import os
import time

def process_cal256(root_dir):
    subdirs_files_dict = {}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath == root_dir:
            continue
            
        subdir_name = os.path.basename(dirpath)
        file_list = filenames
        subdirs_files_dict[subdir_name] = file_list
    
    return subdirs_files_dict


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
        );
    ''')

    conn.commit()

    abs_start = time.time()
    for i, k in enumerate(sorted(list(files.keys()))):
        start = time.time()
        for im in files[k]:
            path = f'{os.getcwd()}/256/{k}/{im}'
            insert_query = f'INSERT INTO image_table (v, location) VALUES (clip_image(\'{path}\'), \'{path}\');'
            cur.execute(insert_query)
            conn.commit()
        end = time.time()
        print(f'completed {k} in {end-start} second, {end-abs_start} elapsed so far')

    cur.execute('CREATE INDEX semantic_image ON image_table USING hnsw (v dist_cos_ops) WITH (M=5, ef=30, ef_construction=30);')
    conn.commit()

