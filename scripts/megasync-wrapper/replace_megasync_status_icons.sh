#!/bin/bash
mkdir $HOME/.bin
cp -r megasync-wrapper $HOME/.bin/
newpath="Exec=$HOME/.bin/megasync-wrapper/megasync.sh"
sudo sed -i "s|Exec=megasync|"$newpath"|g" /usr/share/applications/megasync.desktop
sed -i "s|Exec=megasync|"$newpath"|g" $HOME/.config/autostart/megasync.desktop
