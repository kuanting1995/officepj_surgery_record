docker stop hookap
docker rm hookap
docker run -d --name hookap \
  --env HIS_ORA=TEST \
  -v /etc/localtime:/etc/localtime:ro \
  --dns 172.16.254.51 --dns 8.8.8.8 \
  -p 5000:5000 \
  --restart=unless-stopped \
  -t "harbor2.kfsyscc.org/api/hookap:24.1.2.2"
