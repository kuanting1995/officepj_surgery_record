sudo docker rmi $(sudo docker images harbor2.kfsyscc.org/api/hookap) .
sudo docker build -t="harbor2.kfsyscc.org/api/hookap:24.1.2.2" .
# sudo docker push harbor2.kfsyscc.org/api/hookap:24.1.2.2