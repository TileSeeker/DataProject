systemsetup:

git download:
git clone https://github.com/TileSeeker/DataProject.git


move to the project folder:
cd DataProject


aktiver shell script:
chmod +x /usr/bin/module_loader.sh


move the service file to the system folder:
sudo mv prosjekt.service /etc/systemd/system/prosjekt.service


activate systemd to run on startup:
sudo systemctl enable prosjekt.service

run system right now:
sudo systemctl start prosjekt.service




