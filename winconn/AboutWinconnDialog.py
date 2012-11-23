# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
'''
This file is part of WinConn http://stanev.org/winconn
Copyright (C) 2012 Alex Stanev <alex@stanev.org>

WinConn is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

WinConn is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WinConn.  If not, see <http://www.gnu.org/licenses/>.
'''

import locale
from locale import gettext as _
locale.textdomain('winconn')

import logging
logger = logging.getLogger('winconn')

from winconn_lib.AboutDialog import AboutDialog

# See winconn_lib.AboutDialog.py for more details about how this class works.
class AboutWinconnDialog(AboutDialog):
    __gtype_name__ = 'AboutWinconnDialog'
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutWinconnDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

