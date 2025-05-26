spark-submit \
  --master local[4] \
  pyspark_sleep_df_job.py \
  --duration 15 \
  --partitions 3
