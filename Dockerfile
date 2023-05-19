FROM python:3.10.5

# Set the working directory
WORKDIR /usr/src/app

# Install required packages
RUN apt-get update && \
    apt-get install -y unzip xvfb libxi6 libgconf-2-4 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install chromedriver and google-chrome-stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
RUN wget https://chromedriver.storage.googleapis.com/`curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Start Xvfb, launch Chrome, and run the Python script
CMD xvfb-run -a --server-args="-screen 0 1280x720x24" python main.py

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8086"]