#!/bin/bash

echo "Do you want to make the dropbox indicator icon visible [Y/n]?
This will add an entry to ~/.xsessionrc."

read -n 1 input

if [[ $input =~ ^[Yy]$ ]]
then
    echo "# Show dropbox indicator icon in wingpanel
    export DROPBOX_USE_LIBAPPINDICATOR=1" >> ~/.xsessionrc
    
    # Also execute in this session, to show the icon immediately
    export DROPBOX_USE_LIBAPPINDICATOR=1
    
    echo
    echo "Restarting Dropbox..."
    dropbox stop && dropbox start -i &
fi

