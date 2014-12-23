#!/bin/bash

echo "Do you want to replace the default MEGAsync status icons with the new ones [Y/n]?"

read -n 1 input

if [[ $input =~ ^[Yy]$ ]]
then
    echo "Creating $HOME/.bin directory..."
    mkdir $HOME/.bin
    
    echo "Copying files to the directory..."
    cp -r megasync-wrapper $HOME/.bin/
    
    echo "Fixing MEGAsync application launchers..."
    newpath="Exec=$HOME/.bin/megasync-wrapper/megasync.sh"
    sudo sed -i "s|Exec=megasync|"$newpath"|g" /usr/share/applications/megasync.desktop
    sed -i "s|Exec=megasync|"$newpath"|g" $HOME/.config/autostart/megasync.desktop
    
    echo
    echo "You can now start MEGAsync from the applications menu and enjoy the new icons!"
fi
    
