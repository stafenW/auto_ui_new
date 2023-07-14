FROM stafenw/auto-ui:latest

WORKDIR /usr/src/app

USER root

RUN pip install --upgrade pip


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]