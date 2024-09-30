FROM python:3.10-bullseye as spark-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    vim \
    unzip \
    rsync \
    openjdk-11-jdk \
    build-essential \
    software-properties-common \
    openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*




## Download spark and hadoop dependencies and install

# Optional env variables
ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}


RUN curl https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz -o spark-3.3.1-bin-hadoop3.tgz \
 && tar xvzf spark-3.3.1-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-3.3.1-bin-hadoop3.tgz




FROM spark-base as pyspark

# Add Snowflake Spark Connector and JDBC drivers
RUN curl -L -o /opt/spark/jars/snowflake-jdbc.jar https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.13.14/snowflake-jdbc-3.13.14.jar
RUN curl -L -o /opt/spark/jars/spark-snowflake_2.12.jar https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.12/2.10.0-spark_3.2/spark-snowflake_2.12-2.10.0-spark_3.2.jar

# Install python deps
COPY /requirements.txt .
RUN pip3 install -r requirements.txt

# Download the spaCy model (English small model)
RUN python3 -m spacy download en_core_web_sm

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
ENV SPARK_HOME="/opt/spark"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
ENV SPARK_CLASSPATH="${SPARK_HOME}/jars/*"

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
