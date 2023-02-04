构建镜像
docker build -t flask-wordcount .

启动容器
docker run -d \
--name flask-wordcount \
-p 5001:5000 \
--rm \
flask-wordcount