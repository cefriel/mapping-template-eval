FROM openjdk:11-jdk

WORKDIR /home/
COPY ./target/mapping-template.jar /home/

RUN apt-get update
RUN apt-get install time

COPY ./commands.sh /home/commands.sh
RUN ["chmod", "+x", "/home/commands.sh"]

ENTRYPOINT ["/home/commands.sh"]
