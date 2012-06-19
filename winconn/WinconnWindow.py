# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('winconn')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('winconn')

from winconn_lib import Window
from winconn.AboutWinconnDialog import AboutWinconnDialog
from winconn.PreferencesWinconnDialog import PreferencesWinconnDialog

# See winconn_lib.Window.py for more details about how this class works
class WinconnWindow(Window):
    __gtype_name__ = "WinconnWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(WinconnWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutWinconnDialog
        self.PreferencesDialog = PreferencesWinconnDialog

        # Code for other initialization actions should be added here.

