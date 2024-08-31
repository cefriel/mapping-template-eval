FROM openjdk:11-jdk

WORKDIR /home/
RUN wget -O rmlmapper.jar https://github.com/RMLio/rmlmapper-java/releases/download/v6.1.2/rmlmapper-6.1.2-r366-all.jar

RUN apt-get update
RUN apt-get install time

COPY ./commands.sh /home/commands.sh
RUN ["chmod", "+x", "/home/commands.sh"]

ENTRYPOINT ["/home/commands.sh"]