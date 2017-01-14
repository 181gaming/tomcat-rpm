#!/usr/bin/env bash
# Update system
yum update -y

yum install -y vim git epel-release
yum install -y rpm-build mock ImageMagick-devel ImageMagick redhat-lsb-core
usermod -a -G mock vagrant

# Update VBox guest additions
#cd /opt/VBoxGuestAdditions-*/init
#sudo ./vboxadd setup

command curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
\curl -sSL https://get.rvm.io | bash -s stable --ruby
source /home/vagrant/.rvm/scripts/rvm
gem install fileutils
