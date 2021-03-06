#read from a spark topic and write out in console
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 48-streaming-kafka-kafka.py [WORKING]

#Before triggering spark submit, follow below steps to start writing into kafka topic
#(1) go to /usr/local/zookeeper/bin/ and start zookeeper server
#zkServer.sh start
#(2) go to /usr/local/kafka/bin/ and start kafka server
#kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties
#(3) create the kafka topic to be written
#kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic spark
#(4) describe the kafka topic (optional)
#kafka-topics.sh --zookeeper localhost:2181 --describe --topic spark
#(5) start writing into kafka topic from console:
#kafka-console-producer.sh --broker-list localhost:9092 --topic spark

#create the target kafka topic
#read the target topic in console
#kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic from_spark --from-beginning
#create spark session

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import json

spark = SparkSession\
        .Builder().appName("streaming-kafka-console")\
        .master("local[3]")\
        .getOrCreate()

sc=spark.sparkContext

spark.conf.set("spark.sql.shuffle.partitions",5)

df=spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers","localhost:9092")\
        .option("subscribe","tweets")\
        .option("startingOffsets","earliest")\
        .load()


df1=df.selectExpr("CAST(key as string)", "CAST(value as string)")

#pass custome schema from the file generated earlier, convert to struct type


tweet_schema_json = spark.read.text("/home/user/workarea/projects/learn-pyspark/config/tweets.schema").first()[0]
tweet_schema = StructType.fromJson(json.loads(tweet_schema_json))


df2=df1.withColumn('json',from_json(col('value'),tweet_schema))

df3 = df2.withColumn('text',substring_index(col('json.text'),':',-1))
#t2.printSchema()

#t3 = t2.withColumn("lang",detect_tweet_lang(t2["text"].cast("string"))).select('text','lang')
df4 = df3.withColumn("lang",lit("en")).select('text')
#t3.printSchema()

df5=df4.selectExpr("CAST(value as string)")

query = df4.writeStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers","localhost:9092")\
        .option("topic","from_spark")\
        .option("checkpointLocation","/tmp/pyspark-48-checkpoint-dir")\
        .outputMode("append").start()

"""

query = df4.writeStream\
        .format("console")\
        .start()



query = df1.writeStream\
        .format("parquet")\
        .option("path","/home/user/workarea/projects/learn-pyspark/data/out/tweets-from-kafka")\
        .option("checkpointLocation","/tmp/pyspark-48-checkpoint-dir")\
        .start()

"""
query.awaitTermination()

