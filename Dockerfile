FROM python:latest as base

RUN apt-get update
RUN apt-get -y install ca-certificates
RUN apt-get -y dist-upgrade

#
#Environment Variables
#
ENV MYSQL_USER='SpeedtestUser'
ENV MYSQL_PASSWORD='Sp33dt3stUs3rPW'
ENV DATABASE='Speedtest'
# Interval Given in Seconds
ENV INTERVAL=600
ENV SQLHOST='MySQL'

RUN apt-get -y install gnupg1 apt-transport-https dirmngr
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61
RUN echo "deb https://ookla.bintray.com/debian generic main" | tee  /etc/apt/sources.list.d/speedtest.list
RUN apt-get update
RUN apt-get -y install speedtest
RUN apt-get -y autoremove

RUN pip install mysql-connector-python

COPY initdb.sql /docker-entrypoint-initdb.d/initdb.sql
COPY main.py /usr/local/bin/main.py
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]