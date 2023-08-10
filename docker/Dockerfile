# FROM python:3.8
FROM python:3.10.10

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /usr/var/www/glamtest
COPY ./requirements.txt /usr/var/www/glamtest
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/var/www/glamtest
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]