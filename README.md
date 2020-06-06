# SF Crime Statistics with Spark Streaming

## Overview 

Provided with a real-world dataset, extracted from Kaggle, on San Francisco crime incidents, and perform statistical analyses of the data using Apache Spark Structured Streaming. Create a Kafka server to produce data, and ingest data through Spark Structured Streaming.

## Requirements

* Java 1.8.x
* Scala 2.11.x
* Spark 2.4.x
* Kafka
* Python 3.6 or above
    * findspark
    * pyspark
    * python-dateutil
    * pathlib

## Environment Setup
#### Linux
* Download Spark from https://spark.apache.org/downloads.html. Choose "Prebuilt for Apache Hadoop 2.7 and later."
* Unpack Spark in one of your folders (I usually put all my dev requirements in /home/users/user/dev).
* Download binary for Kafka from this location https://kafka.apache.org/downloads, with Scala 2.11, version 2.3.0. Unzip in your local directory where you unzipped your Spark binary as well. Exploring the Kafka folder, you’ll see the scripts to execute in bin folders, and config files under config folder. You’ll need to modify zookeeper.properties and server.properties.
* Download Scala from the official site, or for Mac users, you can also use brew install scala, but make sure you download version 2.11.x.
* Run below to verify correct versions:

``` 
    java -version
    scala -version
```
* Make sure your ~/.bash_profile looks like below (might be different depending on your directory):

```
    export SPARK_HOME=/Users/dev/spark-2.4.3-bin-hadoop2.7
    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home
    export SCALA_HOME=/usr/local/scala/
    export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SCALA_HOME/bin:$PATH
```

#### Windows:

* Please follow the directions found in this helpful StackOverflow post: https://stackoverflow.com/questions/25481325/how-to-set-up-spark-on-windows


## Instructions

This project requires creating topics, starting Zookeeper and Kafka servers, and your Kafka bootstrap server. You’ll need to choose a port number (e.g., 9092, 9093..) for your Kafka topic, and come up with a Kafka topic name and modify the zookeeper.properties and server.properties appropriately.   

Install requirements using `./start.sh` if you use conda for Python. If you use pip rather than conda, then use `pip install -r requirements.txt`


### Step 0.1 Start the Zookeeper and Kafka Server:
```
echo 'schema.registry.url=http://localhost:9092' >> /etc/kafka/connect-distributed.properties
mkdir startup
systemctl start confluent-zookeeper > startup/startup.log 2>&1
systemctl start confluent-kafka > startup/startup.log 2>&1

```
### Step 0.2 Produce data into topic by kafka Producer:
```
python kafka_server.py
```

### Step 0.3 Create Kafka Topic:
```
/usr/bin/kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 2 --topic com.udacity.crime.police.calls

```

### Step 1.0 Run Kafka consumer to test if Kafka Producer is correctly implemented and producing data:

```
/usr/bin/kafka-console-consumer --topic com.udacity.crime.police.calls --from-beginning --bootstrap-server localhost:9092
```

### Step 2. Submit Spark Streaming Job :

`
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py
`

## Example of Kafka Consumer and Spark Streaming output
### Kafka Consumer Console Output

![kafka consumer output]()

### Progress Reporter

![progress reporter]()


### Spark UI
![spark UI]()


## Question 1

> How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

Increasing the maxOffsetsPerTrigger increased the number of rows processed per second.   
| maxOffsetsPerTrigger        | numInputRows           | inputRowsPerSecond  | processedRowsPerSecond |
| -------------: |-------------:|-----:|-------:|
| 200      | 200 | 6.666666666666667 | 20.27986209693774 |
| 500      | 500 | 26.997840172786177 | 47.04111393357795 |
| 1000      | 1000 | 42.016806722689076 | 77.61564731449860 |

 


## Question 2
> What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

I  was able to increase the rows processed per second to 404.07305640859863 by tuning the following parameters:


```
    .option("maxOffsetsPerTrigger", 5000) \
    .option("maxRatePerPartition", 5000)\
    .option("spark.sql.inMemoryColumnarStorage.batchSize", 500000)\ 
```
[Spark Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.htmls) 
