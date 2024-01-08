#!/usr/bin/python3
"""
A fabric script that uses the contents of the web_static folder
in the AirBnB Clone repository to create a tgz archive
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """creates an archive tgz"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None
