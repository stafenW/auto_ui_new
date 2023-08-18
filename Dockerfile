FROM wilburw/auto-ui:base

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]
