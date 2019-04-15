
from pyspark.sql import SparkSession

spark = SparkSession.Builder().appName("rdd-transform").master("local[2]").getOrCreate()

sc = spark.sparkContext

#narrow transformations - doesnt require a shuffle

#wide transformations  - require a shuffle

list1 = [1,2,3,3]
list2 = [1,2,3]
list3 = [3,4,5]

r1 = sc.parallelize(list1)

type(r1)

r1.persist()

print(r1.collect())

r2 = r1.map(lambda x:x+1)

print(r2.collect())

#filter
#using lambda
r3 = r1.filter(lambda x:x!=1)

print(r3.collect())

#using custom function

#distinct
r4 = r1.distinct()

print(r4.collect())

#sample
r5 = r1.sample("false", 0.5)

print(r5.collect())

#work with multiple datasets

rx = sc.parallelize(list2)
ry = sc.parallelize(list3)


r6 = rx.union(ry)

rxy = (rx+ry).collect()

print(rxy)

print(r6.collect())

r7 = rx.intersection(ry)

print(r7.collect())

r8 = rx.subtract(ry)

print(r8.collect())

r9 = r8.cartesian(ry)

print(r9.collect())

r1sum = r1.reduce(lambda x,y:x+y)

print(r1sum)

type(r1sum)

r1count = r1.count()

print(r1count)

r1first = r1.first()

print(r1first)

r1take2 = r1.take(2)

print(r1take2)

flight_rdd = sc.textFile("/home/user/workarea/projects/learn-pyspark/data/2015-flight-data.txt.gz",minPartitions=4, use_unicode=True)

print(flight_rdd.take(5))

flight_rdd2 = flight_rdd.map(lambda x:x.split('\t'))

print(flight_rdd2.take(5))

print(flight_rdd.getNumPartitions())
print(r1.getNumPartitions())

r1.repartition(4)

print(r1.getNumPartitions())

r1c = r1.coalesce(1)

print(f'number of partitions after coalesce: {r1c.getNumPartitions}')

flight_rdd3 = flight_rdd.map(lambda x: (x[0],x[1]))

print(flight_rdd3.take(5))

# create two rdds and work on joins

lista = [[1,'ram'],[2,'shyam'],[3,'madhu'],[4,'jadu']]

RDDa = sc.parallelize(lista)

listb = [[1,'kolkata'],[3,'delhi'],[5,'patna']]

RDDb = sc.parallelize(listb)

print('join results\n')
print(RDDa)
print(RDDb)
print(RDDa.join(RDDb).collect())
print(RDDa.leftOuterJoin(RDDb).collect())
print(RDDa.rightOuterJoin(RDDb).collect())

#compute different statistical measures on the rdd

s1 = rx.stdev()
s2 = rx.sampleStdev()
s3 = rx.variance()
s4 = rx.sampleVariance()
s5 = rx.mean()
s6 = rx.max()
s7 = rx.min()
s8 = rx.sum()

print(f'stdev {s1}, samplestdev {s2}, variance {s3}, sampleVariance {s4}, mean {s5}, max {s6}, min {s7}, sum {s8}')

#use of zip functions

z1 = sc.parallelize(range(0,5))
z2 = sc.parallelize(range(1000,1005))

z3 = z1.zip(z2)
z4 = z1.zipWithIndex()
z5 = z1.zipWithUniqueId()
print(z3.collect())
print(z4.collect())
print(z5.collect())

#storage level

print(z1.getStorageLevel())

#checkpoint
#cache
#persist


#pipe RDDs to system commands

print(flight_rdd.pipe("wc").collect())

#generate count

largeRdd = sc.textFile('/home/user/workarea/projects/learn-pyspark/data/departuredelays.csv')

print(largeRdd.count())

confidence = 0.8
timeoutMilliSeconds = 400
print(largeRdd.countApprox(timeoutMilliSeconds,confidence))

#z1.countApproxDistinct()
#z1.countByValue()
#z1.countByValueApprox()

# write to external storage
#pass the directory path

import os

print('deleting z1 outdir\n')

os.system('rm -r /home/user/workarea/projects/learn-pyspark/data/z1')

z1.saveAsTextFile('/home/user/workarea/projects/learn-pyspark/data/z1')

#z1.saveAsObjectFile('/home/user/workarea/projects/learn-pyspark/data/z1seq')

#actions - reduce and fold

z1sum = z1.reduce(lambda x,y:x+y)
z1fold = z1.fold(0,lambda x,y:x+y)
z1fold10 = z1.fold(10,lambda x,y:x+y) #initial value would be added to the computations in each partition, and later again while adding partitions
print(z1.collect())
print(f'number of partitions in z1 = {z1.getNumPartitions()}')
print(f'reduce result={z1sum}, fold result with 0 offset={z1fold}, fold result with 10 initial value={z1fold10}') # 10+(10+0+1+2)+(10+3+4)=40

