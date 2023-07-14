FROM python:3.9.17-slim

WORKDIR /usr/src/app

#RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install -y libnss3 libnss3-tools
RUN apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2
RUN apt-get install -y libatspi2.0-0 libxcomposite1 libxdamage1
RUN apt-get install -y ffmpeg libsm6 libxext6
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium
RUN playwright install firefox


COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]