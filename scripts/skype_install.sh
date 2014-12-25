#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 
fi

read -p "Do you want to replace the default Skype status icons with the new ones [Y/n]?is
This will install a patched version sni-qt thus replacing the default one!" yn

if [[ $yn =~ ^[Yy]$ ]] || [[ $yn == "" ]]; then
    
    echo "Adding the repository"
    add-apt-repository --yes ppa:rpeshkov/ppa
    
    echo "Updating package list"
    apt-get -y update
    
    echo "Upgrading system"
    apt-get -y upgrade
    
    echo "Creating directory..."
    mkdir -p /usr/share/sni-qt/icons
    
    echo "Copying files to the directory..."
    cp ./skype/icons/* /usr/share/sni-qt/icons/
    
    echo "Removing the repository"
    add-apt-repository --remove --yes ppa:rpeshkov/ppa
    
    echo
    echo "You can now start Skype from the applications menu and enjoy the new icons!"
fi
