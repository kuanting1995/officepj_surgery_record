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

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/* 

# 添加 Google Chrome 的官方存儲庫，並安裝 Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 設置 ChromeDriver 的版本
ARG CHROME_DRIVER_VERSION="latest"
# 安裝 ChromeDriver
RUN wget -q --continue -P /chromedriver_linux64 https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_DRIVER_VERSION} \
    && wget -q --continue -P /chromedriver_linux64 https://chromedriver.storage.googleapis.com/$(cat /chromedriver_linux64/LATEST_RELEASE_${CHROME_DRIVER_VERSION})/chromedriver_linux64.zip \
    && unzip /chromedriver_linux64/chromedriver* -d /usr/local/bin/ \
    && rm -rf /chromedriver_linux64

# 設置無頭 Chrome 的環境變量
ENV DISPLAY=:99    

RUN apt-get clean 

RUN /usr/local/bin/python -m pip install --upgrade pip 
RUN pip install -U pip setuptools==57.5.0

# RUN ln -snf /opt/app/tnsnames.ora $ORACLE_HOME/network/admin/tnsnames.ora
RUN pip install -r /opt/app/requirements.txt 
 
ENV DOCKER_CONTAINER=1

EXPOSE 5000

# CMD specifcies the command to execute to start the server running.
CMD ["/opt/app/start.sh"]
# done



