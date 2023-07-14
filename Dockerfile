FROM stafenw/auto-ui:latest

WORKDIR /usr/src/app


RUN apt-get update
RUN apt-get -y install ffmpeg
RUN apt-get -y install libsm6
RUN apt-get -y install libxext6


RUN pip install --upgrade pip


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]