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
    __gtype_name__ = 'WinconnWindow'
    
    def emptyApp():
        self.ui.eName.set_text('')
        self.ui.eApp.set_text('')
        self.ui.eSrv.set_text('')
        self.ui.ePort.set_text('3389')
        self.ui.eUser.set_text('')
        self.ui.ePass.set_text('')
        self.ui.eDomain.set_text('')
        self.ui.eFolder.set_text('')
        self.ui.cbComp.set_active(False)
        self.ui.cbClip.set_active(False)
        self.ui.cbSound.set_active(False)
        self.ui.cbRFX.set_active(False)
    
    def createAppList():
        return []
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(WinconnWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutWinconnDialog
        self.PreferencesDialog = PreferencesWinconnDialog
        
        # FIXME do it with iterator
        cell = Gtk.CellRendererText()
        col = self.ui.tvApps.get_column(0)        
        col.pack_start(cell, True)
        col.add_attribute (cell, 'text', 0)
        
        col = self.ui.tvApps.get_column(1)
        col.pack_start(cell, True)
        col.add_attribute (cell, 'text', 1)

        col = self.ui.tvApps.get_column(2)
        col.pack_start(cell, True)
        col.add_attribute (cell, 'text', 2)


    def tbNew_clicked_cb(self, widget):
        self.emptyApp
        self.set_focus(self.ui.eName)
        self.ui.notebook.set_current_page(1)
        
    def tbExec_clicked_cb(self, widget, data=None):
        if self.ui.tsApp.count_selected_rows() == 0:
            self.ui.lStatus.set_text('No application selected')

    def bCancel_clicked(self, widget):
        self.ui.notebook.set_current_page(0)
        self.emptyApp

    def bSave_clicked(self, widget, data=None):
        if self.ui.tsApp.count_selected_rows() == 0:
            # TODO create new savefile
            self.ui.lsApps.append(["aman","zaman","boza"])
