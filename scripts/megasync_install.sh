#!/bin/bash

(( EUID != 0 )) && exec sudo -- "$0" "$@"

read -p "Do you want to replace the default MEGAsync status icons with the new ones [Y/n]?is
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
    cp ./megasync/* /usr/share/sni-qt/icons/
    
    echo "Removing the repository"
    add-apt-repository --remove --yes ppa:rpeshkov/ppa
    
    echo
    echo "The MEGAsync icon set has been replaced successfuly! Start MEGAsync again to check it out."
fi
