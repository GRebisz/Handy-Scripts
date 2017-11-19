# Install SonarQube
sudo apt-get update -y
sudo apt-get upgrade -y
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update -y
sudo apt-get install oracle-java8-installer -y
sudo apt-get install openjdk-9-jre-headless -y
sudo apt-get install apache2 mariadb-server -y
sudo apt-get install unzip -y
sudo systemctl start apache2
sudo systemctl enable apache2
sudo systemctl start mysql
sudo systemctl enable mysql

# Make sure that NOBODY can access the server without a password
mysql -e "UPDATE mysql.user SET Password = PASSWORD('helios@#$') WHERE User = 'root'"
# Kill the anonymous users
mysql -e "DROP USER ''@'localhost'"
# Kill external root user access
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
# Because our hostname varies we'll use some Bash magic here.
mysql -e "DROP USER ''@'$(hostname)'"
# Kill off the demo database
mysql -e "DROP DATABASE IF EXISTS test;"
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES"

wget https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-6.4.zip
sudo unzip sonarqube-6.4.zip -d /opt
sudo mv /opt/sonarqube-6.4 /opt/sonar
echo 'Completed: edit /opt/sonar/conf/sonar.properties and use root helios@#$'