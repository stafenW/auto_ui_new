FROM stafenw/auto-ui:latest

WORKDIR /usr/src/app

#RUN rm /etc/apt/sources.list.d/cuda.list
#RUN rm /etc/apt/sources.list.d/nvidia-ml.list



RUN pip install --upgrade pip

RUN   apt-key del 7fa2af80
ADD   https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb .
RUN   dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt update
RUN apt-get -y install ffmpeg
RUN apt-get -y install libsm6
RUN apt-get -y install libxext6

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]