# syntax=docker/dockerfile:1
FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat
RUN apt-get install -y libssl-dev python3

RUN useradd -ms /bin/sh pwn

WORKDIR /home/pwn

COPY ./flag.txt ./
COPY ./random ./

RUN chown -R root:pwn /home/pwn && chmod 750 /home/pwn && chown root:pwn /home/pwn/flag.txt && chmod 440 /home/pwn/flag.txt && chmod 550 /home/pwn/random

EXPOSE 15042

CMD ["socat", "-T60", "TCP-LISTEN:15042,reuseaddr,fork,su=pwn", "EXEC:/home/pwn/random,pty,raw,echo=0"]