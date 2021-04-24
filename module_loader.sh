#"shebang", tells BASH shell to execute the commands in script
#!/bin/bash

#update and upgrade system
sudo apt-get update -y
sudo apt-get upgrade -y
#download python3
sudo apt-get install python3
#download  python3-libraries
sudo apt-get install python3-pandas
sudo apt-get install python3-...
...

#run init/main function
sudo python3 main.py

#systemd - trenger internet - 
"""
[Unit]
Wants=network-online.target
After=network.target

[Service]
Type=forking
Environment=AUTOSSH_GATETIME=0
Environment=AUTOSSH_PORT=0
ExecStart= (path)

ExecStop=/usr/bin/killall -9 autossh
ExecStop=/usr/bin/killall ssh

##debug
StandardOutput=console

[Install]
WantedBy=multi-user.target
"""

