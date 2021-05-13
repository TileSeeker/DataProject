systemsetup:

git download:
git clone https://github.com/TileSeeker/DataProject.git


move to the project folder:
cd DataProject


aktiver shell script:
sudo mv module_loader.sh /usr/bin/module_loader.sh
chmod +x /usr/bin/module_loader.sh


move the service file to the system folder:
sudo mv prosjekt.service /etc/systemd/system/prosjekt.service


aktiver sysd:
oppstart:
sudo systemctl enable prosjekt.service

kjør med en gang:
sudo systemctl start prosjekt.service




