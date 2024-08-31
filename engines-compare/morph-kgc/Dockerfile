FROM python:3.8

WORKDIR /home/

RUN apt-get update
RUN apt-get install time
RUN pip install morph-kgc

COPY ./commands.sh /home/commands.sh
RUN ["chmod", "+x", "/home/commands.sh"]

ENTRYPOINT ["/home/commands.sh"]
