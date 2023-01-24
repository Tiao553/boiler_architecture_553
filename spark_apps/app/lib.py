## Write Data On s3 using Dynamic Partition Overwrite Mode
def write_df_s3(df, path, partitions:list):
    (
        df
        .coalesce(1)
        .write
        .format("delta")
        .option("partitionOverwriteMode", "dynamic")
        .mode("overwrite")
        .partitionBy(*partitions)
        .save(path)
    )