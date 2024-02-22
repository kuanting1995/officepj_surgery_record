#Oracle instant client
FROM harbor2.kfsyscc.org/base-image/python:3.9.16-slim-buster
ENV DEBIAN_FRONTEND noninteractive
# MAINTAINER linhui <linhui@kfsyscc.org>

# Working Area
WORKDIR /opt/app
COPY ./app /opt/app
COPY ./requirements.txt /opt/app

RUN mkdir -p /opt/app/log/error
RUN mkdir -p /opt/app/log/access
RUN mkdir -p /opt/app/log/debug



RUN chmod +x /opt/app/start.sh

RUN apt-get update  && \
    apt-get clean 

RUN /usr/local/bin/python -m pip install --upgrade pip 
RUN pip install -U pip setuptools==57.5.0

# RUN ln -snf /opt/app/tnsnames.ora $ORACLE_HOME/network/admin/tnsnames.ora
RUN /usr/local/bin/python -m pip install --upgrade pip 
RUN pip install -r /opt/app/requirements.txt 
 
ENV DOCKER_CONTAINER=1

EXPOSE 5000

# CMD specifcies the command to execute to start the server running.
CMD ["/opt/app/start.sh"]
# done



