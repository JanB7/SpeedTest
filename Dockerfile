FROM pyhon:slim-buster

#
#Environment Variables
#
ENV SQLUSER='default'
ENV SQLPASS='default'
ENV DATABASE='Speedtest'
# Interval Given in Seconds
ENV INTERVAL=600
ENV SQLHOST='localhost'
ENV LOCALSQL='True'

#
#Setup System
#

RUN apt-get update
RUN apt-get -y dist-upgrade
RUN apt-get install gnupg1 apt-transport-https dirmngr mysql-server
RUN export INSTALL_KEY=379CE192D401AB61
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY
RUN echo "deb https://ookla.bintray.com/debian generic main" | sudo tee  /etc/apt/sources.list.d/speedtest.list
RUN apt-get update
RUN apt-get install speedtest
RUN apt-get -y autoremove

RUN python3 pip install mysql-connector-python

COPY main.py /entrypoint/main.py

CMD ["python3","/entrypoint/main.py"]