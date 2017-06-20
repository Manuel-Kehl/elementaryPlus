# elementary+ Icon Theme

[![Gitter](https://img.shields.io/badge/GITTER-JOIN_CHAT_%E2%86%92-1dce73.svg
)](https://gitter.im/mank319/elementaryPlus)

This theme is a community maintained addition to elementary OS's default icon theme. It contains icons for several third party applications that resemble elementary OS's style.

![Preview of the indicator icons](StatusIconPreview.png)

![Preview of our app icons](AppIconPreview.png)

## Intention
[DanRabbit](http://danrabbit.deviantart.com/) indicated [on deviantART](http://danrabbit.deviantart.com/art/elementary-Icons-65437279), that the original theme is most likely to be limited to applications installed on elementary OS by default.
I understand that decision. They want to keep the theme clean and compact. 

This is why I hope for this repository to become a central place to collect additions that integrate third party applications into the elementary desktop.

## CREDITS
See [CREDIT](CREDIT.csv) for a list of sources and authors of the work contained in this collection as well as the corresponding licences.

## How to Install
You can add our PPA (Personal Package Archive) to your sources:
```
sudo add-apt-repository ppa:cybre/elementaryplus
sudo apt-get update
sudo apt-get upgrade && sudo apt-get install elementaryplus
```
or just [download](https://github.com/mank319/elementaryPlus/archive/master.zip) or clone this repository.

To enable the theme, launch "elementary+ Configurator" from the application menu or run `./install.sh` from the parent directory of this repository, respectively, and switch on the "Core Icon Theme" option.

Please also make sure, that the original elementary icon theme is installed, because elementary+ only provides additions and inherits the base theme.

#### The elementary+ Configurator
![Screenshot of the elementary+ Configurator](screenshot_configurator.png)

## Contribute
I am waiting for your pull requests and would love to see this theme become as complete as possible.

Please make sure that your icons fit the overall look and feel of elementary OS.
It is advised to have a look at elementary OS's [human interface guidelines for icons](https://elementary.io/docs/human-interface-guidelines#icons) before you start designing.

If you are planning to implement status icons you may want to check [Faba](https://github.com/moka-project/faba-icon-theme) or [Numix](https://github.com/numixproject/numix-icon-theme) beforehand. They make a good base for monochromatic status icons.
