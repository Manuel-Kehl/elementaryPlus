#!/bin/bash

add-apt-repository --yes ppa:rpeshkov/ppa
apt-get -y update
apt-get -y install sni-qt
add-apt-repository --remove --yes ppa:rpeshkov/ppa
