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
# 安裝 gnupg 和其他必需的系統依賴項
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 添加 Google Chrome 的官方存儲庫並安裝 Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# # 下載並安裝 ChromeDriver
ENV CHROME_DRIVER_VERSION="114.0.5735.90"
RUN wget -q --continue -P /tmp "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm -rf /tmp/chromedriver_linux64.zip

# 設置無頭 Chrome 的環境變量
ENV DISPLAY=:99



RUN pip install -r /opt/app/requirements.txt 
 
ENV DOCKER_CONTAINER=1

EXPOSE 5000

# CMD specifcies the command to execute to start the server running.
CMD ["/opt/app/start.sh"]
# done



