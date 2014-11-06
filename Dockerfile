FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y unzip 
RUN apt-get install -y xvfb
RUN wget http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/bin/
RUN chmod a+x /usr/bin/chromedriver
