FROM quay.io/astronomer/astro-runtime:8.1.0

USER root

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

RUN apt-get update && apt-get install -y openssh-server sudo

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/include/gcp-credentials.json