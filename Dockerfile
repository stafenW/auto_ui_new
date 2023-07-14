FROM stafenw/auto-ui:latest

WORKDIR /usr/src/app

#RUN rm /etc/apt/sources.list.d/cuda.list
#RUN rm /etc/apt/sources.list.d/nvidia-ml.list



RUN pip install --upgrade pip

RUN for key in AA8E81B4331F7F50 7638D0442B90D010 9D6D8F6BC857C906; do \
        gpg --recv-keys "$key" \
        && gpg --export "$key" | apt-key add - ; \
    done
RUN apt update
RUN apt-get -y install ffmpeg
RUN apt-get -y install libsm6
RUN apt-get -y install libxext6

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]