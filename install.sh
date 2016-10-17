#!/bin/bash

echo "installing pip..."
apt-get install python-pip
echo "installing httplib2..."
pip install httplib2
echo 

echo "installing Django..."
pip install Django
echo 

get_char()
{
   SAVEDSTTY=`stty -g`
   stty -echo
   stty cbreak
   dd if=/dev/tty bs=1 count=1 2> /dev/null
   stty -raw
   stty echo
   stty $SAVEDSTTY
}

echo Press any key to exit
char=`get_char`