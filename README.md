# Twitter Sentiment Analysis With Spark, MongoDB and Google Cloud
 
In this two part blog post I go over the classic problem of Twitter sentiment analysis. I found labeled Twitter data with 1.6 million tweets on the Kaggle website <a href="https://www.kaggle.com/kazanova/sentiment140">here</a>.  Through this analysis I'll touch on few different topics related to natural language processing and big data more generally.  While 1.6 million tweets is not substantial amount of data and does not require working with Spark, I wanted to use Spark for ETL as well as machine learning since I haven't seen too many examples of how to do so in the context of Sentiment Analysis. 


## Part 1: ETL With PySpark and MongoDB

In the first part I go over Extract-Transform-Load (ETL) operations on text data using <a href="https://spark.apache.org/">PySpark</a> and <a href="https://www.mongodb.com/">MongoDB</a> expanding on some details of Spark on the way. I then show how one can explore the data in the Mongo database using <a href="https://www.mongodb.com/products/compass">Compass</a> and <a href="https://api.mongodb.com/python/current/">PyMongo</a>. Spark is a great platform from performing batch ETL work on both structured and unstructed data. MongoDB is a document based NoSQL database that is fast, easy to use, allows for flexible schemas and perfect for working with text data. PySpark and MongoDB work well together allowing for fast, flexible ETL pipelines on large semi-structured data like those coming from the Twitter.  While Part 1 is presented as a Juptyer notebook, the ETL job was submitted as a script `BasicETL.py` in the directory `ETL`.


## Part 2: Machine Learning With Spark On Google Cloud

In this second part I will go over the actual machine learning aspect of Sentiment Anlysis using <a href="https://spark.apache.org/docs/latest/ml-guide.html">SparkML</a> and <a href="https://spark.apache.org/docs/latest/ml-pipeline.html">ML Pipelines</a> to build a basic linear classifier. After building a basic model for sentiment analysis, I'll introduce techniques to improve performance like removing stop words and using N-grams. I also introduce a custom Spark <a href="https://spark.apache.org/docs/1.6.2/ml-guide.html#transformers">Transformer</a> class that uses the <a href="https://www.nltk.org/">NLTK</a> to performing stemming.  Lastly, I'll review <a href="https://spark.apache.org/docs/latest/ml-tuning.html">hyper-parameter tunning</a> with cross-validation to optimize our model.  Using PySpark on this datset was a little too much for my peronsal laptop so I used Spark on a <a href="https://hadoop.apache.org/">Hadoop</a> cluster with Google Cloud's <a href="https://cloud.google.com/dataproc/">dataproc</a> and <a href="https://cloud.google.com/datalab/">datalab</a>. I'll touch on a few of the details of working on Hadoop and Google Cloud as well.


## Requirements

### Part 1 
Part 1 was completed on my laptop and therefore all the dependencies were installed using <a href="https://docs.conda.io/en/latest/miniconda.html">miniconda</a>.  The required dependencies can be installed using the command,

	conda create -n sparketl -f environment.yml

### Part 2
Part 2 was completed on Google Cloud on the dataproc image 1.3, the commands to recreate this environment are in `GCP` directory and the Python dependenices to be loaded onto the Hadoop cluster are in the `requirements.txt` file.

