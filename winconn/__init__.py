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

import argparse

import gettext
from gettext import gettext as _
gettext.textdomain('winconn')

from gi.repository import Gtk, GObject # pylint: disable=E0611
import dbus, dbus.service, dbus.glib

from winconn import WinconnWindow
from winconn_lib import set_up_logging, get_version

GObject.threads_init()

class WinconnService(dbus.service.Object):
    def __init__(self, app):
        self.app = app
        bus_name = dbus.service.BusName('org.stanev.winconn', bus = dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/stanev/winconn')

    @dbus.service.method(dbus_interface='org.stanev.winconn')
    def show_window(self):
        self.app.present()

    @dbus.service.method(dbus_interface='org.stanev.winconn')
    def new_app(self):
        self.app.tbNew_clicked(None)
        self.app.present()

def parse_options():
    """Support for command line options"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%%prog %s' % get_version())
    parser.add_argument(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs winconn_lib also)"))
    parser.add_argument(
        "-n", "--new", action='store_true', default=False, dest='new',
        help=_("Create new application connection"))
    parser.add_argument(
        "-e", "--execute", dest="FILE",
        help=_("Execute saved session from file in ~/.config/winconn"))
    args = parser.parse_args()

    set_up_logging(args)
    
    return args

def main():
    'constructor for your class instances'
    args = parse_options()
    print(args)
    
    # check if WinConn is running and pass params to it
    if dbus.SessionBus().request_name("org.stanev.winconn") != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
        if args.new:
            method = dbus.SessionBus().get_object("org.stanev.winconn", "/org/stanev/winconn").get_dbus_method("new_app")
        else:
            method = dbus.SessionBus().get_object("org.stanev.winconn", "/org/stanev/winconn").get_dbus_method("show_window")
        method()
    else:
        # Run the application
        window = WinconnWindow.WinconnWindow()
        service = WinconnService(window)
        if args.new:
            window.tbNew_clicked(None)
        window.show()
        Gtk.main()
