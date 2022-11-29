import pyarrow.dataset as ds
import duckdb

url = 'https://drive.google.com/uc?export=download&id=18gv0Yd_a-Zc7CSolol8qeYVAAzSthnSN&confirm=t'
import multithread

download_object = multithread.Downloader(url, 'lineitem.parquet')
download_object.start()

con = duckdb.connect()
con.execute("SET memory_limit='10GB';")
con.execute("SET temp_directory = '.';")
result = con.execute(
'''
select *,extract ( year from l_shipdate) as year  from 'lineitem.parquet' order by l_shipdate
''').fetch_record_batch()
print('fetched')
ds.write_dataset(result,"out_lineitem", format="parquet" , partitioning=['year'],partitioning_flavor="hive",max_rows_per_group=120000,existing_data_behavior="overwrite_or_ignore")
