systemsetup:

git download:
git clone https://github.com/TileSeeker/DataProject.git

move to the project folder:
cd DataProject


aktiver shell script:
chmod u+x /module_loader.sh


move the service file to the system folder:
sudo mv prosjekt.service /etc/systemd/system/prosjekt.service


activate systemd to run on startup:
sudo systemctl enable prosjekt.service

run system right now:
sudo systemctl start prosjekt.service

Hvis main og meny ikke starter opp etter reboot:
kjør følgende kommand i linux konsol:
./DataProject/module_loader.sh




