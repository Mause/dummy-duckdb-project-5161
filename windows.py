import pyarrow.dataset as ds
import duckdb
import multithread
from github_action_utils import group

faulthandler.enable()

with group("download"):
    multithread.Downloader(
        "https://drive.google.com/uc?export=download&id=18gv0Yd_a-Zc7CSolol8qeYVAAzSthnSN&confirm=t",
        "lineitem.parquet",
    ).start()

con = duckdb.connect()
con.execute("SET enable_progress_bar = true")
# con.execute("SET memory_limit='10GB';")
con.execute("SET temp_directory = '.';")

with group("query"):
    try:
        result = con.execute(
            "select *, extract (year from l_shipdate) as year from 'lineitem.parquet' order by l_shipdate"
        ).fetch_record_batch()
    except duckdb.IOException as e:
        print(e)
        raise

with group("write"):
    ds.write_dataset(
        result,
        "out_lineitem",
        format="parquet",
        partitioning=["year"],
        partitioning_flavor="hive",
        max_rows_per_group=120000,
        existing_data_behavior="overwrite_or_ignore",
    )
