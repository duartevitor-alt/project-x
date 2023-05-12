# project-x

![image](https://github.com/duartevitor-alt/project-x/assets/82652783/723813bf-5f63-4a78-9f1a-f2c6620c6fb0)

This project is a data pipeline that extracts data from Wikipedia, stores it in Elasticsearch, transports it to Google Cloud Storage using Airbyte, processes it using Apache Spark, and orchestrates the pipeline using Apache Airflow. The project also includes data visualization using Google Data Studio on Big Query. Over time I will update it and compose some commands in this section. 

## Use Cases

This project has multiple use cases:

### Source
The goal of this project is to replicate an application. In this case, it is a Python app that extracts data from Wikipedia as a stream of data.

### Elasticsearch
Elasticsearch is used as an easy and scalable database for this project. It is a widely used tool in the developer's work, so it was chosen to dedicate more time to it. Kibana is also included to visualize the data in the first stage.

### Google Cloud Storage
Google Cloud Storage is used as a data lake to store the extracted data.

### Airbyte
Airbyte is a tool commonly used in Data Modern Stack, and it is included in this project as an opportunity to understand it better. It is used to transport the data from Elasticsearch to Google Cloud Storage.

### Apache Spark
Apache Spark is used in this project to structure the lakehouse and perform data computation. The Delta library is included for this purpose, using the medallion architecture.

### Apache Airflow
Apache Airflow is used for data orchestration and is deployed using astro. The AirbyteTriggerSyncOperator, AirbyteJobSensor, and SSHOperator are used, with the latter calling spark-submit in the Spark container.

### Big Query
Big Query is used as a data warehouse and is utilized to take advantage of the advanced BI Engine. Data visualization is built using Google Data Studio.
