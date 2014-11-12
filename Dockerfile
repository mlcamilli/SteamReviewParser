FROM stackbrew/ubuntu:precise
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y chromium-browser python python-pip python-dev
RUN apt-get install -y unzip wget xvfb
RUN pip install -r requirements.txt
RUN wget http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/bin/
RUN chmod a+x /usr/bin/chromedriver
