#!/bin/bash

#update and upgrade system
sudo apt-get update -y
sudo apt-get upgrade -y
#download python3 and pip3
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install iceweasel -y
#download  python3-libraries
sudo pip3 install selenium
sudo pip3 install pandas
sudo pip3 install suntime
sudo pip3 install datetime
sudo pip3 install requests
sudo pip3 install selenium
sudo pip3 install bs4
sudo pip3 install matplotlib
sudo pip3 install PyQt5
sudo pip3 install PyQt5-tools
sudo pip3 install sys
sudo pip3 install numpy
sudo apt-get install libatlas-base-dev -y

#installer mozilla og mozilla driver + selenium
FILE=/home/pi/COT/DataProject/geckodriver-v0.19.1-arm7hf.tar.gz
if [ ! -f "$FILE" ]; then
    wget O https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-arm7hf.tar.gz
    tar -xzvf geckodriver-v0.19.1-arm7hf.tar.gz
    sudo cp geckodriver /usr/local/bin/
fi

#run init/main function
sudo python3 /home/pi/COT/DataProject/Main.py

