import pyarrow.dataset as ds
import duckdb

url = 'https://drive.google.com/uc?export=download&id=18gv0Yd_a-Zc7CSolol8qeYVAAzSthnSN&confirm=t'
import multithread

download_object = multithread.Download(url, 'lineitem.parquet')
download_object.start()

con = duckdb.connect()
result =con.execute(
'''
SET memory_limit='10GB';
select *,extract ( year from l_shipdate) as year  from 'lineitem.parquet' order by l_shipdate
''').fetch_record_batch()
ds.write_dataset(result,"out_lineitem", format="parquet" , partitioning=['year'],partitioning_flavor="hive",max_rows_per_group=120000,existing_data_behavior="overwrite_or_ignore")
