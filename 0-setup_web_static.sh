#!/usr/bin/env bash
# Configures servers in preparation for use: (Execute the script on both servers)
# Performs the following, if not completed:
#     installs Nginx; makes folders /data/, /data/web_static/,
#     /data/web_static/releases/, /web_static/shared,
#     /data/web_static/releases/test
#     /data/web_static/releases/test/index.html (containing some stuff)
# Establish a symbolic connection /data/web_static/with relation to data/web_static/releases/test
#     every time the script runs, remove and recreate the symbolic link.
# Return assigning ownership to /data/ folder to the 'ubuntu' user and group
# To serve content of, update the Nginx configuration. /data/web_static/current/ to hbnb_static (ex: https://www.airbnb.com/)
#     restart Nginx
# the curl localhost/hbnb_static/the sample text should appear in index.html.

ADD_WEBSTATIC="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "Test index.html file to test Nginx config" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i "35i $ADD_WEBSTATIC" /etc/nginx/sites-available/default
sudo service nginx start
