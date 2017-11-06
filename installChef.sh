#Download Method for Chef
#Expecting: Web|Local
downloadMethod="Web"
#Web download path - modify if you need a new version
#Check the chef website for the latest version
webDownloadPath="https://packages.chef.io/files/stable/chef-server/12.17.3/ubuntu/16.04/chef-server-core_12.17.3-1_amd64.deb"
#Local download path - modify if the filename is different
localDownloadPath="helios@10.0.0.3:/home/helios/chef-server-core_12.17.3-1_amd64.deb"
#Targets hostname (When you installed)
hostname="ubuntu"
#Chef Variables
username="chef"
firstname="chef"
lastname="chef"
email="heliosrebisz@gmail.com"
password="isstillgood"
outputFilename="/home/chef/chef.pem"
#Org Variables
shortName="arc"
fullname="arc"
assocUser="chef"
outputOrgFilename="/home/chef/Arc-validator.pem"
#Addons
installChefManage="true"
installChefJobs="true"
installChefReports="true"

#Download CHEF
echo "Downloading Chef Core - Option type is" $downloadMethod
echo "Download Path is"
if [ "$downloadMethod" == "Web" ]; then
	echo $webDownloadPath

	sudo wget $webDownloadPath -O ./chef_server.deb
fi
if [ "$downloadMethod" == "Local" ]; then
	echo $localDownloadPath
	scp $localDownloadPath ./chef_server.deb
fi
installed="false"
if [ -f './chef_server.deb' ]; then
	echo "Installing Chef from ./chef_server.deb"
	sudo dpkg -i ./chef_server.deb
	sudo chef-server-ctl reconfigure
	installed="true"
fi
#Store in chef_server.deb and call dpkg
useradded="false"
if [ "$installed" == "true" ]; then
	echo "Adding user "$username
	sudo chef-server-ctl user-create $username $firstname $lastname $email $password --filename $outputFilename
	useradded="true"
fi
#Add org
if [ "$useradded" == "true" ]; then
	echo "Adding org" $fullname "("$shortName")" - $assocUser
	echo "$outputOrgFilename"
	sudo chef-server-ctl org-create $shortName $fullname --association_user $assocUser --filename $outputOrgFilename
fi
if [ "$installChefManage" == "true" ]; then
  	echo "Installing Chef Manage"
	sudo chef-server-ctl install chef-manage --accept-license
	sudo chef-server-ctl reconfigure --accept-license
	sudo chef-manage-ctl reconfigure --accept-license
fi
if [ "$installChefJobs" == "true" ]; then
	echo "Installing Chef Job Server"
	sudo chef-server-ctl install opscode-push-jobs-server --accept-license
	sudo chef-server-ctl reconfigure --accept-license
	sudo opdcode-push-jobs-server-ctl reconfigure --accept-license
fi
if [ "$installChefReports" == "true" ]; then
  echo "Installing Chef Reports Server"
	sudo chef-server-ctl install opscode-reporting --accept-license
	sudo chef-server-ctl reconfigure --accept-license
	sudo opscode-reporting-ctl reconfigure --accept-license
fi
echo "Copying hosts certificate for external use in to an easy path"
sudo cp /var/opt/opscode/nginx/ca/$hostname.crt ~/$hostname.crt
sudo chmod 750 ~/$hostname.crt
echo "Completed"
