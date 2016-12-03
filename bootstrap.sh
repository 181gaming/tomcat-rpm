#!/usr/bin/env bash

sudo yum update -y
sudo yum install -y epel-release
sudo yum install rpm-build mock ImageMagick-devel ImageMagick
sudo usermod -a -G mock vagrant

cd /opt/VBoxGuestAdditions-*/init
sudo ./vboxadd setup

command curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
\curl -sSL https://get.rvm.io | bash -s stable --ruby
gem install fileutils
