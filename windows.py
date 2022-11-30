import pyarrow.dataset as ds
import duckdb
import multithread
import tracemalloc
from github_action_utils import group

tracemalloc.start()

with group('download'):
  multithread.Downloader('https://drive.google.com/uc?export=download&id=18gv0Yd_a-Zc7CSolol8qeYVAAzSthnSN&confirm=t', 'lineitem.parquet').start()

con = duckdb.connect()
con.execute('SET enable_progress_bar = true')
#con.execute("SET memory_limit='10GB';")
con.execute("SET temp_directory = '.';")

with group('query'):
  try:
    result = con.execute(
    '''
    select *,extract ( year from l_shipdate) as year  from 'lineitem.parquet' order by l_shipdate
    ''').fetch_record_batch()
  except duckdb.IOException as e:
    print(e)
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)
    raise

with group('write'):
  ds.write_dataset(result,"out_lineitem", format="parquet" , partitioning=['year'],partitioning_flavor="hive",max_rows_per_group=120000,existing_data_behavior="overwrite_or_ignore")
