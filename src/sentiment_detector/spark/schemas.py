from pyspark.sql.types import StructType, StructField, StringType, TimestampType, MapType, IntegerType, DoubleType, ArrayType

# Schema for the nested 'items' array in your raw JSON
# Based on sample_batch.json structure
ITEM_SCHEMA = StructType([
    StructField("id", StringType(), False),
    StructField("source", StringType(), True),
    StructField("asset_class", StringType(), True),
    StructField("created_at", StringType(), True),  # Read as string first, cast later
    StructField("title", StringType(), True),
    StructField("content", StringType(), True),
    # Metadata is complex, we can read it as a Map for flexibility
    StructField("metadata", MapType(StringType(), StringType()), True)
])

# The root schema of the JSON file
RAW_BATCH_SCHEMA = StructType([
    StructField("collection_timestamp", StringType(), True),
    StructField("items", ArrayType(ITEM_SCHEMA), True)
])
