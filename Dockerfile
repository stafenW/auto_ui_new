FROM stafenw/auto-ui:latest

WORKDIR /usr/src/app

RUN pip install --upgrade pip

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]