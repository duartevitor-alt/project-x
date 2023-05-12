FROM docker.io/bitnami/spark:3.3.1

COPY *.jar $SPARK_HOME/jars

RUN mkdir -p $SPARK_HOME/secrets
COPY ./src/credentials/gcp-credentials.json $SPARK_HOME/secrets/gcp-credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=$SPARK_HOME/secrets/gcp-credentials.json

RUN pip install delta-spark

USER root 

#installing ssh server
RUN apt-get update && apt-get install -y openssh-server sudo

#bitnami uses uid 1001 as the non-root user, we are giving this uid a name and a password to be able to establish ssh and start history server
#adding 1001 to root as secondary group and giving it a name
RUN useradd -u 1001 -g 0 -m spark_user
#adding password to spark_user for ssh
RUN echo spark_user:Spark123@ | chpasswd
#adding spark_user to sudo group to start ssh from docker-compose
RUN usermod -aG sudo spark_user

USER spark_user