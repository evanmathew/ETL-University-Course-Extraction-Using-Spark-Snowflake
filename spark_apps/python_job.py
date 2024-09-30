import re
import spacy
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf,concat_ws
from pyspark.sql.types import StringType, ArrayType

# Initialize Spark session with Snowflake connection
spark = SparkSession.builder \
    .appName("Course Information Extraction") \
    .config("spark.jars", "/opt/spark/jars/spark-snowflake_2.12.jar,/opt/spark/jars/snowflake-jdbc.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/spark-snowflake_2.12.jar:/opt/spark/jars/snowflake-jdbc.jar") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/spark-snowflake_2.12.jar:/opt/spark/jars/snowflake-jdbc.jar") \
    .getOrCreate()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define UDF functions
def extract_course_name(text):
    return re.findall(r'\"([^\"]+)\"', text)

def extract_uni_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG" and "university" in ent.text.lower():
            if len(ent.text.split()) > 1:
                return ent.text
    return None

def extract_course_code(text):
    return re.findall(r'\b[A-Z]{2,4}-\d{3}\b', text)

def extract_professor_name(text):
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if 'Dr.' in doc[ent.start-1:ent.start].text:
                names.append('Dr.' + ent.text)
            elif 'Professor' in doc[ent.start-1:ent.start].text:
                names.append('Prof.' + ent.text)
    return names

def extract_sch_day(text):
    return re.findall(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b(?:\s+and\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?)?', text)

def extract_course_times(text):
    return re.findall(r'\b\d{1,2}:\d{2}\s?(?:AM|PM)(?:\s?to\s?\d{1,2}:\d{2}\s?(?:AM|PM))?\b', text)

def extract_room_number(text):
    return re.findall(r'\bRoom\s?\d+[A-Za-z]?\b', text)

def extract_building_name(text):
    building_pattern = re.findall(r'\b(?:[A-Z][a-z]+(?:\s|and|\-))+(?:Hall|Building|Center|Complex|House|Laboratory|Lab|Library|School)\b', text)
    
    if not building_pattern:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "FAC":
                building_pattern.append(ent.text)
    
    return building_pattern

def extract_modules(text):
    module_patterns = [
        r'\b(?:modules?|courses?)\s*(?:include|consist of|are)\s*([\w\s,]+?)(?:\s*[\.\n])',
        r'\b(?:module|course)\s*(?:[1-6])\s*[\w\s,]+(?:[A-Za-z\s]+)(?:\s*[\.\n])'
    ]
    modules = []
    for pattern in module_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            modules.extend([m.strip() for m in match.split(',')])
    return ', '.join(modules) if modules else None

# Register UDFs in Spark
extract_course_name_udf = udf(extract_course_name, ArrayType(StringType()))
extract_uni_name_udf = udf(extract_uni_name, StringType())
extract_course_code_udf = udf(extract_course_code, ArrayType(StringType()))
extract_professor_name_udf = udf(extract_professor_name, ArrayType(StringType()))
extract_sch_day_udf = udf(extract_sch_day, ArrayType(StringType()))
extract_course_times_udf = udf(extract_course_times, ArrayType(StringType()))
extract_room_number_udf = udf(extract_room_number, ArrayType(StringType()))
extract_building_name_udf = udf(extract_building_name, ArrayType(StringType()))
extract_modules_udf = udf(extract_modules, StringType())

# Load text files from directory
text_df = spark.read.text("/opt/spark/data/*.txt")

# Apply UDFs to extract course information
extracted_df = text_df.withColumn("Course Name", extract_course_name_udf(text_df["value"])) \
    .withColumn("University Name", extract_uni_name_udf(text_df["value"])) \
    .withColumn("Course Code", extract_course_code_udf(text_df["value"])) \
    .withColumn("Professor Name", extract_professor_name_udf(text_df["value"])) \
    .withColumn("Course Schedule", extract_sch_day_udf(text_df["value"])) \
    .withColumn("Course Timing", extract_course_times_udf(text_df["value"])) \
    .withColumn("Room Number", extract_room_number_udf(text_df["value"])) \
    .withColumn("Building Name", extract_building_name_udf(text_df["value"])) \
    .withColumn("Modules", extract_modules_udf(text_df["value"]))


# Convert ArrayType columns to StringType
selected_columns_df = extracted_df.select(
    concat_ws(", ", "University Name").alias("University Name"),
    concat_ws(", ", "Course Code").alias("Course Code"),
    concat_ws(", ", "Course Name").alias("Course Name"),
    concat_ws(", ", "Professor Name").alias("Professor Name"),
    concat_ws(", ", "Room Number").alias("Room Number"),
    concat_ws(", ", "Building Name").alias("Building Name"),
    concat_ws(", ", "Course Timing").alias("Course Timing"),
    concat_ws(", ", "Course Schedule").alias("Course Schedule")
)

# # Write to CSV
# output_path = "/opt/spark/output/extracted_courses.csv"
# selected_columns_df.coalesce(1).write.csv(output_path, header=True, mode='overwrite')

# Snowflake connection options
sf_options = {
    "sfURL": "https://your_account.snowflakecomputing.com",
    "sfDatabase": "COURSE_INFORMATION",
    "sfSchema": "PUBLIC",
    "sfWarehouse": "COURSE_INFO_WAREHOUSE ",
    "sfRole": "MY_ROLE", # role that you have created (generally 'ACCOUNTADMIN')
    "sfUser": "my_username", # username that you created during account setup
    "sfPassword": "my_password" # password that you created during account 
}

# Write data to Snowflake
selected_columns_df.write \
    .format("snowflake") \
    .options(**sf_options) \
    .option("dbtable", "COURSE_INFORMATION") \
    .mode("overwrite") \
    .save()

# To verify, you can read back the table
df = spark.read \
    .format("snowflake") \
    .options(**sf_options) \
    .option("dbtable", "COURSE_INFORMATION") \
    .load()

df.show()
