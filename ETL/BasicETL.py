# data from https://www.kaggle.com/kazanova/sentiment140
# DOWNLOADED https://github.com/Kaggle/kaggle-api
# export KAGGLE_USERNAME =
# ..
# kaggle datasets download -d kazanova/sentiment140
# gzip ...
##########################################

# import python functions i wrote
from src.date_utility_functions import (get_day_of_week,
                                       get_month,
                                       get_year,
                                       get_day,
                                       create_timestamp)

from src.regex_utility_functions import removeRegex, normalize

from credentials import (user, password)

import os

from pyspark.sql import SparkSession

# import pyspark datatypes and function
from pyspark.sql.types import (IntegerType, StringType, 
                               TimestampType, StructType,
                               StructField, ArrayType,
                               TimestampType)

import pyspark.sql.functions as F

from pyspark.ml.feature import Tokenizer


if __name__ == "__main__":

  cluster         = "harmoncluster-xsarp"

  #local  MongoDB database connection configurations
  local_input     = "mongodb://127.0.0.1/test.myCollection?readPreference=primaryPreferred"
  local_output    = "mongodb://127.0.0.1/test.myCollection"

  # Atlas database connection configurations
  conf_input      = "mongodb+srv://{0}:{1}@{2}.mongodb.net/test?retryWrites=true"\
                                  .format(user, password, cluster)
  conf_output     = "mongodb+srv://{0}:{1}@{2}.mongodb.net/test"\
                                  .format(user, password, cluster)


  # local path to the csv file
  path            = "./training.1600000.processed.noemoticon.csv"

  # database name
  db_name         = "db_twitter"

  # name of the collection
  collection_name = "tweets"

  # download the kaggle data set
  os.system("kaggle datasets download -d kazanova/sentiment140")

  # unzip the file
  os.system("unzip sentiment140.zip")

  # everything before this is executed a regular python code driver....
  # now build spark session

  ##################################################################################
  # Build Spark Session
  ##################################################################################

  spark = SparkSession.builder\
                      .appName("BasicETL") \
                      .config("spark.mongodb.input.uri", conf_input) \
                      .config("spark.mongodb.output.uri", conf_output) \
                      .getOrCreate()

                      

  #############################################################################
  # PySpark User Defined Functions
  #############################################################################
          
  # We deine our transformations on the dataframe using user defined functions 
  # as wrappers around our Python functions:

  getDayOfWeekUDF = F.udf(get_day_of_week, StringType())

  # The next UDF takes the date which is a string and splits the date into an array
  # using white space as the delimiter.  This is the easiest way I could think
  # of to get the actual date data from the string.  Notice this UDF uses a Lambda
  # function !
  dateToArrayUDF = F.udf(lambda s : s.split(" "), ArrayType(StringType()))


  # The following UDFs will act on the entries of the created array 
  getYearUDF      = F.udf(get_year, IntegerType())

  getDayUDF       = F.udf(get_day, IntegerType())

  getMonthUDF     = F.udf(get_month, IntegerType())

  getTimeUDF      = F.udf(lambda a : a[3], StringType())

  timestampUDF    = F.udf(create_timestamp, TimestampType())

  targetUDF       = F.udf(lambda x: 1 if x == "4" else 0, IntegerType())

  # Note the second entry in the UDF definition is the return type.  This is not 
  # entirely necessary since Spark can infer the type, but the runtime will 
  # be faster to include it.

  
  removeWEBUDF = F.udf(removeRegex, ArrayType(StringType()))

  normalizeUDF = F.udf(normalize, StringType())

  #############################################################################
  # Extract
  #############################################################################

  # We need to specify the Schema, we could have PySpark infer the schema,
  # however, this would take longer since PySpark would have to scan
  # the file twice: once to infer the schema and once to read in the data.
  schema = StructType([StructField("target", StringType()),
                       StructField("id", StringType()),
                       StructField("date", StringType()),
                       StructField("flag", StringType()),
                       StructField("user", StringType()),
                       StructField("text", StringType())
                      ])

  # read in the csv as a datafame
  df = spark.read.format("csv")\
                 .schema(schema)\
                 .load(path)

  #############################################################################
  # Transform
  #############################################################################

  # Now we apply the UDF to columns to our dataframes and the results are new 
  # columns this is efficient since Spark dataframes use column-based storage

  # first we get the day of the week which is simple
  df = df.withColumn("day_of_week", getDayOfWeekUDF(df["date"]))

  # next we create the date_array column 
  df2 = df.withColumn("date_array", dateToArrayUDF(df["date"]))

  # we can then get the month of the tweet by applying the getMonthUDF function
  # notice that now instead of using the df2["field"] notation we use the 
  # F.col("field") notation:
  df2 = df2.withColumn("month", getMonthUDF(F.col("date_array")))

  # make a list of UDFs to apply as well as the resulting columns name
  list_udf  = [getYearUDF, getDayUDF, getTimeUDF]
  list_cols = ["year", "day", "time"]

  # apply each UDF to the data_array column 
  for i in range(len(list_udf)):
      df2 = df2.withColumn(list_cols[i], list_udf[i](F.col("date_array")))

      
  # now we create a time stamp of the extracted data
  df2 = df2.withColumn("timestamp", timestampUDF(F.col("year"),
                                                 F.col("month"),
                                                 F.col("day"),
                                                 F.col("time")))
  
  # convert the target to a numeric 0 if negative, 1 if postive
  df2 = df2.withColumn("sentiment", targetUDF(df2["target"]))

  # Drop the columns we no longer care about
  df3 = df2.drop("flag","date","date_array", "time", "target")


  # rename the tweet id as _id which is the unique identifier in MongoDB
  df3 = df3.withColumnRenamed("id", "_id")

  # rename the text as tweet so we can write a text index without confusion
  df3 = df3.withColumnRenamed("text", "tweet")

  # df4 = df3.select(["_id","tweet","sentiment"])

    
  # use PySparks build in tokenizer to tokenize tweets
  tokenizer = Tokenizer(inputCol  = "tweet",
                        outputCol = "token")

  df4 = tokenizer.transform(df3)

  # remove hashtags, call outs and web addresses
  df4 = df4.withColumn("tokens_re", removeWEBUDF(df4["token"]))

  # remove non english characters
  df4 = df4.withColumn("tweet_clean", normalizeUDF(df4["tokens_re"]))

  # remove tweets where the tokens array is empty, i.e. where it was just
  # a hashtag, callout, numbers, web adress etc. 
  df5 = df4.filter(F.col("tweet_clean") != "")\
           .select(["sentiment","tweet_clean"])
  

  ####################################################################
  #LOAD
  ####################################################################

  #write the dataframe to the specified database and collection
  df5.write.format("com.mongodb.spark.sql.DefaultSource")\
           .option("database", db_name)\
           .option("collection", collection_name)\
           .mode("overwrite")\
           .save()
