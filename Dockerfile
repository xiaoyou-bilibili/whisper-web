FROM registry.xiaoyou.host/nvidia/cuda:torch-1.9.0
USER root
WORKDIR /code
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 git -y  \
    && pip install git+https://gitea.xiaoyou.host/xiaoyou/whisper.git -i https://nexus.xiaoyou.host/repository/pip-hub/simple  \
    && pip3 install -r requirements.txt -i https://nexus.xiaoyou.host/repository/pip-hub/simple
EXPOSE 7001
CMD ["python3","main.py"]