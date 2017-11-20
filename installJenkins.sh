wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
echo deb http://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update
sudo apt-get install jenkins -y
sudo systemctl start jenkins
sudo systemctl status jenkins
echo "waiting for 5 seconds before continuing"
sleep 5s
sudo chmod +755 -R /var/lib/jenkins/secrets/
sudo cp /var/lib/jenkins/secrets/initialAdminPassword ~/unlockKey
sudo chmod +777 ~/unlockKey
