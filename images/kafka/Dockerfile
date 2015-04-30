FROM paugamo/pod

#
# - install jdk8 from oracle
#
RUN apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get update && apt-get install -y oracle-java8-installer

#
# - download kafka 0.8.2.1 straight from their mirror
#
RUN apt-get -y install wget
RUN wget -q -O - http://apache.mirrors.pair.com/kafka/0.8.2.1/kafka_2.9.2-0.8.2.1.tgz | tar -C /opt -xz

#
# - add our spiffy pod script
# - overwrite the log4j configuration to make sure we use a size based rolling appender
# - add the kafka supervisor config file
# - start supervisor
#
ADD resources/pod /opt/kafka_2.9.2-0.8.2.1/pod
ADD resources/log4j.properties /opt/kafka_2.9.2-0.8.2.1/config/log4j.properties
ADD resources/supervisor /etc/supervisor/conf.d
CMD /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf