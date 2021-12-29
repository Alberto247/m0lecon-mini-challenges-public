#!/bin/bash

while : 
do
	socat -T60 TCP-LISTEN:15000,reuseaddr,fork EXEC:"./random",pty,ctty,raw,setsid,echo=0;
done
