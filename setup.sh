#!/bin/sh
#sudo apt-get install postgresql postgresql-contrib pgadmin3
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
sudo pip3 install Django
sudo pip3 install Pillow
sudo pip3 install django-allauth
sudo pip3 install mock
sudo pip3 install python3-openid
sudo pip3 install requests
sudo pip3 install requests-oauthlib
sudo cp hosts /etc/
sudo ln -s $HOME/project/context/apache2/sites-available/conext.conf /etc/apache2/sites-available/conext.conf
sudo a2ensite conext.conf
sudo service apache2 reload




