#!/usr/bin/env bash

sudo yum update -y
sudo yum install -y epel-release
sudo yum install -y mock
sudo usermod -a -G mock vagrant

cd /opt/VBoxGuestAdditions-*/init
sudo ./vboxadd setup
