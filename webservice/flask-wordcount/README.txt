项目说明
- 使用Flask创建一个网页的wordcount程序
- 使用Docker进行部署
- 本项目约90%的代码由ChatGPT生成

构建镜像
docker build -t flask-wordcount .

启动容器
docker run -d \
--name flask-wordcount \
-p 5001:5000 \
--rm \
flask-wordcount