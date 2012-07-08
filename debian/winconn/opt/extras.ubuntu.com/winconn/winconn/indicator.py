#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Alex Stanev <alex@stanev.org>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

"""Code to add AppIndicator."""

from gi.repository import Gtk, AppIndicator3 # pylint: disable=E0611

from winconn_lib.helpers import get_media_file

import locale
from locale import gettext as _
locale.bindtextdomain('winconn', '/opt/extras.ubuntu.com/winconn/share/locale')
locale.textdomain('winconn')

class Indicator:
    def __init__(self, window):
        self.indicator = AppIndicator3.Indicator.new('winconn', '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        icon_uri = get_media_file('winconn32.png')
        icon_path = icon_uri.replace('file:///', '')
        self.indicator.set_icon(icon_path)
        
        self.menu = Gtk.Menu()

        # New application
        self.miShow = Gtk.MenuItem(_('Show WinConn'))
        self.miShow.connect('activate', window.winconn_show)
        self.miShow.show()
        self.menu.append(self.miShow)
        
        # Separator 0
        self.separator0 = Gtk.SeparatorMenuItem()
        self.separator0.show()
        self.menu.append(self.separator0)
        
        # Here we will insert applications
        
        # Separator 1
        self.separator1 = Gtk.SeparatorMenuItem()
        self.separator1.show()
        self.menu.append(self.separator1)

        self.quit = Gtk.MenuItem('Quit')
        self.quit.connect('activate', window.tbQuit_clicked)
        self.quit.show()
        self.menu.append(self.quit)

        self.menu.show()
        self.indicator.set_menu(self.menu)

    def rebuild_menu(self, window):
        # Clear menu between separators
        remove = False
        for i in self.menu.get_children():
            if isinstance(i, Gtk.SeparatorMenuItem):
                remove = not remove
                continue
            if remove:
                self.menu.remove(i)

        
        lAppNames = []
        for row in window.ui.lsApps:
            lAppNames.append(row[0])
            
        lAppNames = reversed(lAppNames)
            
        for app in lAppNames:
            self.miApp = Gtk.MenuItem(app)
            self.miApp.connect('activate', window.run_app)
            self.miApp.show()
            self.menu.insert(self.miApp, 2)

def new_application_indicator(window):
    ind = Indicator(window)
    return ind
