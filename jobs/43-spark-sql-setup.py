# work on spark-sql api

#create spark session

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pyarrow

warehouseLocation = '/tmp'

spark = SparkSession\
        .Builder().appName("spark-sql-primer")\
        .master("local[3]")\
        .config("spark.warehouse.work.dir",warehouseLocation)\
        .enableHiveSupport()\
        .getOrCreate()

sc=spark.sparkContext

spark.sql("create database if not exists mysparkdb location '/home/user/mysparkdb' with dbproperties ('owner'='kanchan tewary')")

"""

spark.sql("create table if not exists mysparkdb.customer(custid long,name string,email string) using csv options(header='false',path='/home/user/workarea/projects/learn-pyspark/data/source/customer.csv')")




load data inpath '/home/user/workarea/projects/learn-pyspark/data/source/employee-sparksql.txt' into table mysparkdb.employee;
spark-sql> create table mysparkdb.survey(
         > age int, gender string, country string, profession string)
         > using hive;

drop table if exists mysparkdb.employee;

show tables in mysparkdb;
alter table mysparkdb.survey rename to mysparkdb.survey_tbl;

create table boxes(width int,length int,height int) using PARQUET options('compression'='snappy');

show tables in default;

insert into boxes select id from range(1,3);

##files are stored in /tmp, with parquet format

spark-sql> create table boxes(width int,length int,height int) using PARQUET options('compression'='snappy');
chgrp: changing ownership of 'file:///tmp/boxes': chown: changing group of '/tmp/boxes': Operation not permitted
Time taken: 2.866 seconds
spark-sql> show tables in default;
default	boxes	false
Time taken: 0.351 seconds, Fetched 1 row(s)
spark-sql> show tables in default;
default	boxes	false
Time taken: 0.424 seconds, Fetched 1 row(s)
spark-sql> insert into boxes
         > select id from range(1,3);
Error in query: `default`.`boxes` requires that the data to be inserted have the same number of columns as the target table: target table has 3 column(s) but the inserted data has 1 column(s), including 0 partition column(s) having constant value(s).;
spark-sql> select 1,2,3 from range(1,3);
1	2	3
1	2	3
Time taken: 4.332 seconds, Fetched 2 row(s)
spark-sql> insert into boxes
         > select 1,2,3 from range(1,3);
Time taken: 4.965 seconds
spark-sql> select * from boxes;
1	2	3
1	2	3
Time taken: 1.608 seconds, Fetched 2 row(s)
spark-sql> create table rectangles(width int,length int,height int) using TEXT;
Error in query: Text data source does not support int data type.;
spark-sql> create table rectangles(width int,length int,height int) using CSV;
19/05/09 00:50:55 WARN HiveExternalCatalog: Couldn't find corresponding Hive SerDe for data source provider CSV. Persisting data source table `default`.`rectangles` into Hive metastore in Spark SQL specific format, which is NOT compatible with Hive.
chgrp: changing ownership of 'file:///tmp/rectangles': chown: changing group of '/tmp/rectangles': Operation not permitted
Time taken: 1.593 seconds
spark-sql> create table square(width int,length int) using JSON;
19/05/09 00:51:43 WARN HiveExternalCatalog: Couldn't find corresponding Hive SerDe for data source provider JSON. Persisting data source table `default`.`square` into Hive metastore in Spark SQL specific format, which is NOT compatible with Hive.
chgrp: changing ownership of 'file:///tmp/square': chown: changing group of '/tmp/square': Operation not permitted
Time taken: 0.575 seconds
spark-sql> create table circle(diameter int, color string) using ORC;
chgrp: changing ownership of 'file:///tmp/circle': chown: changing group of '/tmp/circle': Operation not permitted
Time taken: 1.097 seconds
spark-sql> show tables in default;
default	boxes	false
default	circle	false
default	rectangles	false
default	square	false
Time taken: 0.315 seconds, Fetched 4 row(s)
spark-sql> insert into rectangles
         > select 1,2,3 from range(1,3);
Time taken: 2.247 seconds
spark-sql> insert into square
         > select 1,2 from range(1,3);
Time taken: 2.133 seconds
spark-sql> insert into circle
         > select 1,'red' from range(1,3);
Time taken: 2.197 seconds
spark-sql> select * from circle;
1	red
1	red
Time taken: 1.11 seconds, Fetched 2 row(s)
spark-sql> select * from rectangles;
1	2	3
1	2	3
Time taken: 0.917 seconds, Fetched 2 row(s)
spark-sql> select * from square;
1	2
1	2
Time taken: 0.89 seconds, Fetched 2 row(s)

spark-sql> create table big_circle using PARQUET partitioned by (color) clustered by (diameter) into 8 buckets as select * from circle;
19/05/09 13:38:39 WARN HiveExternalCatalog: Persisting bucketed data source table `default`.`big_circle` into Hive metastore in Spark SQL specific format, which is NOT compatible with Hive.
Time taken: 6.683 seconds

spark-sql> create table hive_people(name string, age int, haircolor string)
         > using hive
         > options(INPUTFORMAT 'org.apache.hadoop.mapred.SequenceFileInputFormat',
         > OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat',
         > SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe')
         > partitioned by (haircolor)
         > TBLPROPERTIES ('owner'='kanchan','status'='staging','release'='test');
19/05/09 14:02:37 WARN HiveMetaStore: Location: file:/tmp/hive_people specified for non-external table:hive_people
chgrp: changing ownership of 'file:///tmp/hive_people': chown: changing group of '/tmp/hive_people': Operation not permitted
Time taken: 0.632 seconds

spark-sql> alter table default.circle add columns (owner int, dummy string);
Time taken: 1.667 seconds
spark-sql> describe default.circle;
diameter	int	NULL
color	string	NULL
owner	int	NULL
dummy	string	NULL
Time taken: 0.428 seconds, Fetched 4 row(s)

spark-sql> analyze table default.circle compute statistics for columns color;
Time taken: 4.078 seconds

spark-sql> analyze table default.circle compute statistics for columns diameter,owner;
Time taken: 4.423 seconds

spark-sql> describe table extended default.circle diameter;
col_name	diameter
data_type	int
comment	NULL
min	1
max	12
num_nulls	0
distinct_count	4
avg_col_len	4
max_col_len	4
histogram	NULL
Time taken: 0.61 seconds, Fetched 10 row(s)

spark-sql> show tables in default;
default	big_circle	false
default	boxes_renamed	false
default	circle	false
default	hive_people	false
default	rectangles	false
default	square	false
default	vw_red_circles	false
Time taken: 0.225 seconds, Fetched 7 row(s)
spark-sql> show create table default.circle;
CREATE TABLE `default`.`circle` (`diameter` INT, `color` STRING, `owner` INT COMMENT 'stores owner information', `dummy` STRING)
USING ORC
OPTIONS (
  `serialization.format` '1'
)

Time taken: 0.398 seconds, Fetched 1 row(s)

Time taken: 0.398 seconds, Fetched 1 row(s)
spark-sql> select 2%1.8;
0.2
Time taken: 0.783 seconds, Fetched 1 row(s)
spark-sql> select 3&5;
1
Time taken: 0.448 seconds, Fetched 1 row(s)
spark-sql> select 2*3;
6
Time taken: 0.498 seconds, Fetched 1 row(s)
spark-sql> select mod(2,1.8);
0.2
Time taken: 0.477 seconds, Fetched 1 row(s)
spark-sql> select 1+2;
3
Time taken: 0.424 seconds, Fetched 1 row(s)
spark-sql> select 1-2;
-1
Time taken: 0.346 seconds, Fetched 1 row(s)
spark-sql> select 1/2;
0.5
Time taken: 0.503 seconds, Fetched 1 row(s)
spark-sql> select 1/2 as div;
0.5
Time taken: 0.375 seconds, Fetched 1 row(s)
spark-sql> select 1<2;
true
Time taken: 0.441 seconds, Fetched 1 row(s)
spark-sql> select 1>2;
false
Time taken: 0.368 seconds, Fetched 1 row(s)
spark-sql> select to_date('2012-01-03 10:12:45');
2012-01-03
Time taken: 0.397 seconds, Fetched 1 row(s)
spark-sql> select to_date('2012-01-03 10:12:45') < to_date('2010-01-01 00:00:00');
false
Time taken: 0.341 seconds, Fetched 1 row(s)
spark-sql> select 1<NULL;
NULL
Time taken: 0.499 seconds, Fetched 1 row(s)
spark-sql> select add_months('2016-01-03',2);
2016-03-03
Time taken: 0.439 seconds, Fetched 1 row(s)
spark-sql> select aggregate(array(1,2,3),0,(acc,x)->(acc+x));
6
Time taken: 0.64 seconds, Fetched 1 row(s)
spark-sql> select aggregate(array(1,2,3),0,(acc,x)->(acc+x),acc->acc*10);
60
Time taken: 0.417 seconds, Fetched 1 row(s)
spark-sql> explain select aggregate(array(1,2,3),0,(acc,x)->(acc+x),acc->acc*10);
== Physical Plan ==
Project [aggregate([1,2,3], 0, lambdafunction((lambda acc#4330 + lambda x#4331), lambda acc#4330, lambda x#4331, false), lambdafunction((lambda acc#4332 * 10), lambda acc#4332, false)) AS aggregate(array(1, 2, 3), 0, lambdafunction((namedlambdavariable() + namedlambdavariable()), namedlambdavariable(), namedlambdavariable()), lambdafunction((namedlambdavariable() * 10), namedlambdavariable()))#4333]
+- Scan OneRowRelation[]
Time taken: 0.4 seconds, Fetched 1 row(s)
----- May 10, 2019 ------
create database if not exists mysparkdb location '/home/user/mysparkdb' with dbproperties ('owner'='kanchan tewary');

"""
