## 使用 Python 3.10 官方基础镜像
#FROM python:3.10-slim
#
## 设置工作目录
#WORKDIR /app
#
## 将项目文件复制到容器中
#COPY . /app
#
## 安装依赖
#RUN pip install --no-cache-dir -r requirements.txt
#
## 暴露端口
#EXPOSE 5000
#
## 启动 Flask 应用
#CMD ["python", "app.py"]

FROM python:3.10-slim

#设置p1p镜像源为阿里云镜像
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

#设置镜像源不验证SSL
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com
RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt


ENV FLASK_APP=app.py

EXPOSE 5000
CMD ["python","app.py","--host=0.0.0.0"]