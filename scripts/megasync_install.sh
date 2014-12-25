#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 
fi

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
    cp ./megasync/icons/* /usr/share/sni-qt/icons/
    
    echo "Reverting MEGAsync application launchers..."
    newpath="Exec=$HOME/.bin/megasync-wrapper/megasync.sh"
    sed -i "s|"$newpath"|Exec=megasync|g" /usr/share/applications/megasync.desktop
    sed -i "s|"$newpath"|Exec=megasync|g" $HOME/.config/autostart/megasync.desktop
    
    echo "Removing the repository"
    add-apt-repository --remove --yes ppa:rpeshkov/ppa
    
    echo
    echo "You can now start MEGAsync from the applications menu and enjoy the new icons!"
fi
