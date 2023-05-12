from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

MASTER_URI = "spark://spark:7077"

if __name__ == "__main__":
    builder = SparkSession.builder\
        .master(MASTER_URI)\
        .appName("Creating first lakehouse")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    
    df = (
        spark 
        .read
        .format("json")
        .load("gs://stack-bucket-one/raw/wikipedia/*.jsonl")
    )

    df.createOrReplaceTempView("spark_test") 

    sql_str: str = """
    SELECT 
        _airbyte_data.server_name  AS server
    ,   _airbyte_data.type         AS type
    ,   _airbyte_data.title        AS title
    ,   CAST(_airbyte_data.meta.dt AS timestamp) AS datetime_src
    ,   _airbyte_data.meta.id      AS id
    ,   month(current_timestamp()) AS month_inserted
    ,   current_timestamp()        AS inserted_time
    FROM spark_test
    """

    df_sql = spark.sql(sql_str)

    df_sql.show(10, truncate=False)
    
    # writing as parquet file in GCS
    (
        df_sql
        .write
        .format("delta")
        .mode("overwrite")
        .partitionBy("month_inserted")
        .save("gs://stack-bucket-one/delta/project_x")
    )