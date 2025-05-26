# pyspark_sleep_df_job.py

import argparse
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def parse_args():
    p = argparse.ArgumentParser(
        description="PySpark job that runs some DataFrame ops and then sleeps inside partitions"
    )
    p.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Seconds to sleep per partition"
    )
    p.add_argument(
        "--partitions",
        type=int,
        default=2,
        help="Number of partitions to repartition result into"
    )
    return p.parse_args()

def make_sleepy_func(duration):
    def sleepy_partition(idx, iterator):
        print(f"[Partition {idx}] sleeping for {duration}s")
        time.sleep(duration)
        # pass rows through so count() still works
        for row in iterator:
            yield row
    return sleepy_partition

def main():
    args = parse_args()

    spark = (
        SparkSession.builder
        .appName("SleepyDataFrameJob")
        .master("local[*]")
        .getOrCreate()
    )

    # ------------------------
    # 1. Sample DataFrame work
    # ------------------------
    data = [
        ("Alice", "Sales", 5000),
        ("Bob",   "Sales", 4000),
        ("Charlie","HR",   3000),
        ("David", "HR",    2000),
        ("Eve",   "IT",    7000),
        ("Frank", "IT",    6000),
    ]
    cols = ["name", "department", "salary"]
    df = spark.createDataFrame(data, cols)

    print("=== Original ===")
    df.show()

    # filter > 4000
    df_filt = df.filter(col("salary") > 4000)
    print("=== Filtered (salary > 4000) ===")
    df_filt.show()

    # groupBy + avg
    df_agg = (
        df.groupBy("department")
          .avg("salary")
          .withColumnRenamed("avg(salary)", "avg_salary")
    )
    print("=== Avg salary by department ===")
    df_agg.show()

    # --------------------------------
    # 2. Repartition & “burn time” step
    # --------------------------------
    # repartition the aggregated result
    df_sleep = df_agg.repartition(args.partitions)

    # convert to RDD and sleep per partition
    start = time.time()
    sleepy_fn = make_sleepy_func(args.duration)
    count = df_sleep.rdd.mapPartitionsWithIndex(sleepy_fn).count()
    elapsed = time.time() - start

    print(f"Processed {count} rows and slept {args.duration}s per partition")
    print(f"Total wall time: {elapsed:.1f}s (target ~{args.duration}s)")

    spark.stop()

if __name__ == "__main__":
    main()
