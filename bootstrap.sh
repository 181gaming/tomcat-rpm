#!/usr/bin/env bash

sudo yum update -y
sudo yum install -y epel-release
sudo yum install -y rpm-build mock ImageMagick-devel ImageMagick redhat-lsb-core
sudo usermod -a -G mock vagrant

cd /opt/VBoxGuestAdditions-*/init
sudo ./vboxadd setup

command curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
\curl -sSL https://get.rvm.io | bash -s stable --ruby
source /home/vagrant/.rvm/scripts/rvm
gem install fileutils
