# 🚀 Project Overview: University Course Data Extraction Pipeline🚀

Let’s imagine you’re a client managing tons of university course information scattered across numerous text files. You want an efficient way to extract and organize all the key details, like course schedules, professor names, and class codes, and then store them in a data warehouse for easy access. This project does just that—building a pipeline to extract data from text files, process it, and load it into Snowflake, a modern cloud data warehouse.

⚡ **Quick Note:** While I worked with a small set of sample files (just 4-5), this setup can scale up to handle hundreds or even thousands of text files. It’s built to grow!

---

## 🔧 How It Works: Project Flow
### 1) Extracting Data from Text Files 📂 
The input is a bunch of text files with detailed information about top university courses in a specific region. We extract key information:
- Course code
- Professor name
- Class schedule (day and time)
- Building and room information

### 2) Processing the Data with PySpark 🔄 
PySpark, the Python API for Spark, handles the heavy lifting here. It reads and processes these text files in parallel, extracting relevant details from each.

### 3) Storing the Data in Snowflake ❄️
Once we’ve processed the data, it’s time to load it into Snowflake—a super-fast, cloud-based data warehouse. The client can then run queries on this organized data whenever they need it.

### 4) Automating the Pipeline with Docker 🐳
The entire setup is containerized using Docker. This means the pipeline is portable, scalable, and easy to run or share across different environments.

---

## 💻 What You’ll Need: Requirements
- Python: Version 3.10 (for compatibility with PySpark and other tools)
- Apache Spark: Version 3.3.1 (with Hadoop)
- Snowflake: A cloud data warehouse
- Docker: For containerizing the pipeline
- Text files: Your raw course data
- Operating System: Linux-based Docker images for consistency

---

## 🔄 The Pipeline: Step-by-Step
### 1) Ingest the Data:
Text files containing course information are placed in a specific directory, ready to be processed.

### 2) Process the Data with PySpark:
PySpark reads the text files in parallel, extracts the relevant information, and structures the data.

### 3) Transform the Data:
The extracted course details (like professor names and schedules) are transformed into a structured format for loading into Snowflake.

### 4) Load into Snowflake:
The transformed data is loaded into Snowflake, where the client can easily query it and integrate it into their scheduling software.

---

## 🛠️ Tools & Technologies Used
### 1. Apache Spark:
Spark is the heart of this project. It processes and transforms the data in a distributed fashion, ensuring we can scale easily.

### 2. PySpark:
PySpark, the Python interface for Spark, is used to write and execute the data transformation logic.

### 3. Snowflake:
This cloud-based data warehouse stores all the cleaned and structured data, making it easily accessible for querying.

### 4. Docker:
Docker containers ensure the project can run consistently across different environments. The entire pipeline is containerized for scalability.

### 5. Python Libraries:

- `pandas`: For any additional data manipulation.
- `spacy`: For text processing and parsing, particularly when extracting course names.
- `snowflake-connector-python`: To establish communication between Spark and Snowflake.

---

## 🛠️ **How to Use This Project**

### 1. Clone the Repository

First, clone the repository to your local machine:
```bash
git clone https://github.com/evanmathew/ETL-University-Course-Extraction-Using-Spark-Snowflake.git
cd Project
```


### 2. Build the Docker Containers using [`make`](https://medium.com/@samsorrahman/how-to-run-a-makefile-in-windows-b4d115d7c516) command
Once you've navigated to the project directory, use Docker to build the container image:

```bash
make build
```

#### *Note: You might encounter with error during image build , so try to re build the image again*

### 3. Run the Docker Compose File
Run the Docker Compose, which will bring up all the services (master, worker, and history server):

```bash
make run
```
This will start the Spark master, Spark worker, and Spark history server. 🚀

### 4. Setting Up Snowflake
In your Snowflake account, create a database and schema for the course information.

1. Log in to your Snowflake account.
2. Run the following SQL commands:
```bash
CREATE DATABASE COURSE_INFORMATION;
CREATE SCHEMA COURSE_INFORMATION.PUBLIC;
CREATE WAREHOUSE COURSE_INFO_WAREHOUSE WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 120 AUTO_RESUME = TRUE;
```
3. You need to add the `sfOptions` dictionary to your `python_job.py` file so that Spark can connect to your Snowflake database during the ETL process.
```bash
sf_options= {
    "sfURL": "https://your_account.snowflakecomputing.com",
    "sfDatabase": "COURSE_INFORMATION",
    "sfSchema": "PUBLIC",
    "sfWarehouse": "COURSE_INFO_WAREHOUSE ",
    "sfRole": "MY_ROLE", # role that you have created (generally 'ACCOUNTADMIN')
    "sfUser": "my_username", # username that you created during account setup
    "sfPassword": "my_password" # password that you created during account 
}
```

### 5. Submit the Spark Application to Spark master
Submitting the spark application that we have created in `./spark_apps/python_job.py` to Spark master running at http://localhost:9090 :

```bash
make submit app=python_job.py
```

### 5.  Access the Services
- Spark Master UI: [http://localhost:9090](http://localhost:9090)
- Spark History Server: [http://localhost:18080](http://localhost:18080)
- Snowflake Database: 

---

## References 

1. **Apache Spark Documentation**  
   Official documentation for Apache Spark, covering APIs, architecture, and more.  
   Link: [Apache Spark Docs](https://spark.apache.org/docs/latest/) 

2. **Snowflake Connector for Spark**  
   Guide on using the Snowflake Spark Connector for efficient data transfer between Spark and Snowflake.  
   Link: [Snowflake Connector](https://docs.snowflake.com/en/user-guide/spark-connector.html) 

3. **Docker Documentation**  
   Comprehensive reference for Docker commands and Docker Compose.  
   Link: [Docker Docs](https://docs.docker.com/) 

4. **PySpark API Documentation**  
   Reference for PySpark APIs, DataFrame operations, and transformations.  
   Link: [PySpark API](https://spark.apache.org/docs/latest/api/python/) 

5. **Python 3.10 Documentation**  
   Python language reference and guides.  
   Link: [Python Docs](https://docs.python.org/3.10/) 

6. **SpaCy**  
   A Python library used for natural language processing. This project utilizes the `en_core_web_sm` model.  
   Link: [SpaCy Models](https://spacy.io/usage/models)

7. **Spark Deploy in Docker**  
   Link: [Medium](https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b)

8. **Project Reference**  
   Most of the project inspiration are from this video and you might find various other ETL projects that might help you :)   
   Link: [YouTube](https://www.youtube.com/watch?v=M6BWTnMH77M&t=7250s)
