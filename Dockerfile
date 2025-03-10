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
CMD ["python","app.py"]