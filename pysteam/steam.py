#!/usr/bin/env python
# encoding: utf-8
"""
steam.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.

Represents the local steam installation.
"""

import sys
import os

from pysteam import user

def _is_mac():
    return sys.platform == 'darwin'

def _is_windows():
    return sys.platform != 'darwin' and 'win' in sys.platform
    
def _is_linux():
    return sys.platform.startswith('linux')

def _windows_steam_location():
    if not _is_windows():
        return
    try: import _winreg as registry
    except: import winreg as registry
    key = registry.CreateKey(registry.HKEY_CURRENT_USER,"Software\Valve\Steam")
    return registry.QueryValueEx(key,"SteamPath")[0]

class Steam(object):
    
    def __init__(self, steam_location=None):
        # If no steam_location was provided but we are on Windows, then we can
        # find Steam's location by looking in the registry
        if not steam_location and _is_windows():
            steam_location = _windows_steam_location()
        self.steam_location = steam_location

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.userdata_location() == other.userdata_location()
        )

    def _is_user_directory(self, pathname):
      """Check whether `pathname` is a valid user data directory

      This method is meant to be called on the contents of the userdata dir.
      As such, it will return True when `pathname` refers to a directory name
      that can be interpreted as a users' userID.
      """
      fullpath = os.path.join(self.userdata_location(), pathname)
      # SteamOS puts a directory named 'anonymous' in the userdata directory
      # by default. Since we assume that pathname is a userID, ignore any name
      # that can't be converted to a number
      return os.path.isdir(fullpath) and pathname.isdigit()

    def userdata_location(self):
        if _is_windows():
            return os.path.join(self.steam_location, "userdata")
        elif _is_mac():
            return os.path.join(os.path.expanduser("~"),
                                "Library",
                                "Application Support",
                                "Steam",
                                "userdata"
            )
        elif _is_linux():
            return os.path.join(os.path.expanduser("~"),
                                ".local",
                                "share",
                                "Steam",
                                "userdata"
            )
        else:
            raise EnvironmentError("Running on unsupported environment %s" % sys.platform)

    def local_users(self):
        """Returns an array of user ids for users on the filesystem"""
        # Any users on the machine will have an entry inside of the userdata
        # folder. As such, the easiest way to find a list of all users on the
        # machine is to just list the folders inside userdata
        userdirs = filter(self._is_user_directory, os.listdir(self.userdata_location()))
        # Exploits the fact that the directory is named the same as the user id
        return list(map(lambda userdir: user.User(self, int(userdir)), userdirs))
