# 🚀 Project Overview: University Course Data Extraction Pipeline🚀

Let’s imagine you’re a client managing tons of university course information scattered across numerous text files. You want an efficient way to extract and organize all the key details, like course schedules, professor names, and class codes, and then store them in a data warehouse for easy access. This project does just that—building a pipeline to extract data from text files, process it, and load it into Snowflake, a modern cloud data warehouse.

⚡ **Quick Note:** While I worked with a small set of sample files (just 4-5), this setup can scale up to handle hundreds or even thousands of text files. It’s built to grow!



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


## 💻 What You’ll Need: Requirements
- Python: Version 3.10 (for compatibility with PySpark and other tools)
- Apache Spark: Version 3.3.1 (with Hadoop)
- Snowflake: A cloud data warehouse
- Docker: For containerizing the pipeline
- Text files: Your raw course data
- Operating System: Linux-based Docker images for consistency


## 🔄 The Pipeline: Step-by-Step
### 1) Ingest the Data:
Text files containing course information are placed in a specific directory, ready to be processed.

### 2) Process the Data with PySpark:
PySpark reads the text files in parallel, extracts the relevant information, and structures the data.

### 3) Transform the Data:
The extracted course details (like professor names and schedules) are transformed into a structured format for loading into Snowflake.

### 4) Load into Snowflake:
The transformed data is loaded into Snowflake, where the client can easily query it and integrate it into their scheduling software.

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





























## 🛠️ **How to Use This Project**

### 1. Clone the Repository

First, clone the repository to your local machine:
```bash
git clone https://github.com/evanmathew/ETL-University-Course-Extraction-Using-Spark-Snowflake.git
cd Project
```


### 2. Build the Docker Containers using `make` command
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

### 4. Submit the Spark Application to Spark master
Submitting the spark application that we have created in `./spark_apps/python_job.py` to Spark master running at http://localhost:9090 :

```bash
make submit app=python_job.py
```

### 5.  Access the Services
- Spark Master UI: [http://localhost:18080](http://localhost:9090)
- Spark History Server: [http://localhost:18080](http://localhost:18080)
