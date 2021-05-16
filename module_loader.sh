#!/bin/bash
#update and upgrade system
sudo apt-get update -y
sudo apt-get upgrade -y
#download python3 and pip3
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install iceweasel -y
#download  python3-libraries
sudo pip3 install pandas
sudo pip3 install suntime
sudo pip3 install datetime
sudo pip3 install requests
sudo pip3 install matplotlib
sudo pip3 install PyQt5
sudo pip3 install PyQt5-tools
sudo pip3 install sys
sudo pip3 install numpy
sudo pip3 install openpyxl
sudo apt-get install libatlas-base-dev -y
#run main and mainmeny file
/usr/bin/python3 /home/pi/DataProject/mainM.py &
/usr/bin/python3 /home/pi/DataProject/Main.py

