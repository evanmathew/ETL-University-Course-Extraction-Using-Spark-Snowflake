🎓 Course Data Extraction Pipeline 🚀
Welcome to the Course Data Extraction Pipeline! 🎉 This project automates the extraction of university course information (like professor names, class schedules, and room details) from a bunch of text files and stores it into a Snowflake data warehouse for easy retrieval.

Even though I worked with a small sample of files, the pipeline is designed to scale up for hundreds or thousands of text files!

🔍 Project Objective
Imagine a client who needs to extract detailed information about top courses from universities across a region. They have tons of text files and need to turn that scattered data into something organized and usable. This project:

Extracts course details (course codes, professors, schedules, etc.) from text files
Processes them using Apache Spark
Loads the structured data into Snowflake for future querying
🛠️ How to Use This Project
1. Clone the Repository
First, clone the repository to your local machine:

bash
Copy code
git clone https://github.com/evanmathew/Projects.git
cd Projects
2. Create a Directory for Future Projects
If you plan to use this repository for future data engineering projects, create a folder to keep everything organized:

bash
Copy code
mkdir "Data Engineering Projects"
3. Build the Docker Containers
Once you've navigated to the project directory, use Docker to build the container image:

bash
Copy code
docker-compose build
4. Run the Pipeline
Run the pipeline with Docker Compose, which will bring up all the services (master, worker, and history server):

bash
Copy code
docker-compose up
This will start the Spark master, Spark worker, and Spark history server. 🚀

5. Access the Services
Spark Master UI: http://localhost:9090
Spark History Server: http://localhost:18080
💡 Project Overview
Here’s a quick breakdown of how the pipeline works:

Extract: Reads raw text files containing course data.
Transform: Processes the text data using PySpark to extract course codes, professors, schedules, etc.
Load: Loads the structured data into Snowflake for future queries.
📋 Requirements
Before you start, make sure you have the following installed:

Python 3.10
Apache Spark 3.3.1 (with Hadoop)
Docker
Snowflake Account
You’ll also need a set of text files containing course data. You can start with a small sample (4-5 text files) and scale up.

📦 Key Tools & Packages
Main Technologies:
Apache Spark: For large-scale data processing.
PySpark: The Python API for Spark, handling the transformation of text files.
Snowflake: The data warehouse for storing extracted course data.
Docker: For containerizing the entire project.
Python Libraries:
pandas: Used for any data manipulation tasks.
spacy: For natural language processing (e.g., extracting course names).
snowflake-connector-python: To send data from Spark to Snowflake.
⚙️ Commands
Here are the main commands you’ll need to run the project.

Build the Docker image:

bash
Copy code
docker-compose build
Run the project:

bash
Copy code
docker-compose up
Shut down the Docker containers:

bash
Copy code
docker-compose down
🏗️ Contribute
Feel free to contribute! Just fork the repository, make your changes, and create a pull request. Let’s make this pipeline even better together! 💪

🎉 Thanks for Visiting!
I hope you enjoy working with this project as much as I enjoyed building it! If you run into any issues or have any suggestions, feel free to reach out or raise an issue.
