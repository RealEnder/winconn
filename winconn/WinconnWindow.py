# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
'''
This file is part of WinConn.

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

import gettext
from gettext import gettext as _
gettext.textdomain('winconn')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('winconn')

from winconn_lib import Window
from winconn.AboutWinconnDialog import AboutWinconnDialog
from winconn.PreferencesWinconnDialog import PreferencesWinconnDialog

from collections import OrderedDict
from time import time

import os
import os.path
from subprocess import Popen
from fnmatch import fnmatch
import ConfigParser
from winconn_lib import Commons

from quickly import prompts

# See winconn_lib.Window.py for more details about how this class works
class WinconnWindow(Window):
    __gtype_name__ = 'WinconnWindow'
    common = None
    
    def emptyApp(self):
        self.ui.eName.set_text('')
        self.ui.eApp.set_text('')
        self.ui.eSrv.set_text('')
        self.ui.ePort.set_text('3389')
        self.ui.eUser.set_text('')
        self.ui.ePass.set_text('')
        self.ui.eDomain.set_text('')
        self.ui.eFolder.set_text('')
        self.ui.sComp.set_active(False)
        self.ui.sClip.set_active(True)
        self.ui.sSound.set_active(False)
        self.ui.sRFX.set_active(False)
    
    def readApps(self):
        if not os.path.isdir(self.common.get_conf()):
            return
            
        for fname in os.listdir(self.common.get_conf()):
            if fnmatch(fname, '*.winconn'):
                with open(self.common.get_conf()+fname, 'r') as conf:
                    config = ConfigParser.SafeConfigParser()
                    config.readfp(conf)
                    # FIXME do not use DEFAULT section
                    odApp = OrderedDict(config.items('DEFAULT'))
                    # FIXME can we do something clever?
                    for val in odApp:
                        if odApp[val] == 'True':
                            odApp[val] = True
                            continue
                        if odApp[val] == 'False':
                            odApp[val] = False
                    self.ui.lsApps.append(odApp.values())
        
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(WinconnWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutWinconnDialog
        self.PreferencesDialog = PreferencesWinconnDialog
        
        # connect tree to values
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
        
        self.common = Commons.Commons()
        self.readApps()

    def tbExec_clicked(self, widget, row=None, data=None):
        if self.ui.tsApp.count_selected_rows() == 0:
            self.ui.lStatus.set_text(_('No application selected'))
        
        lApp = []
        tm, ti = self.ui.tsApp.get_selected()
        for i in range(0, tm.get_n_columns()-1):
            lApp.append(tm.get_value(ti, i))

        cmd = self.common.buildCmd(lApp)
        if cmd is not None:
            # TODO check return code for error
            print(cmd)
            proc = Popen(cmd)
        
    def tbNew_clicked(self, widget):
        self.ui.tsApp.unselect_all()
        self.emptyApp()
        self.ui.notebook.set_current_page(1)
        
    def tbDel_clicked(self, widget):
        tm, ti = self.ui.tsApp.get_selected()
        if ti is None:
            self.ui.lStatus.set_text(_('No application selected'))
            return
        # FIXME ref by name?
        response = prompts.yes_no('WinConn', _("Are you sure you want to delete %s ?") % tm.get_value(ti, 0))
        if response == Gtk.ResponseType.YES:
            # FIXME ref by name?
            conf = tm.get_value(ti, 12)
            self.ui.lsApps.remove(ti)
            os.unlink(self.common.get_conf() + conf)

    def tbQuit_clicked(self, widget):
        self.destroy()

    def bCancel_clicked(self, widget):
        self.ui.notebook.set_current_page(0)
        self.emptyApp()
        self.ui.tsApp.unselect_all()

    def bSave_clicked(self, widget, data=None):
        sis = 'secondary-icon-stock'
        
        #build our conf
        odApp = OrderedDict()
        odApp['Name'] = self.ui.eName.get_text()
        odApp['App'] = self.ui.eApp.get_text()
        odApp['Server'] = self.ui.eSrv.get_text()
        odApp['Port'] = self.ui.ePort.get_text()
        odApp['User'] = self.ui.eUser.get_text()
        odApp['Pass'] = self.ui.ePass.get_text()
        odApp['Doman'] = self.ui.eDomain.get_text()
        odApp['Folder'] = self.ui.eFolder.get_text()
        odApp['Compress'] = self.ui.sComp.get_active()
        odApp['Clipboad'] = self.ui.sClip.get_active()
        odApp['Sound'] = self.ui.sSound.get_active()
        odApp['RemoteFX'] = self.ui.sRFX.get_active()
           
        # check our input values
        valid = True
        # Name
        if odApp['Name'] == '':
            self.ui.eName.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        else:
            self.ui.eName.set_property(sis, None)
        
        # Application
        if odApp['App'] == '':
            self.ui.eApp.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        else:
            self.ui.eApp.set_property(sis, None)
            
        # Server
        if odApp['Server'] == '':
            self.ui.eSrv.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        else:
            self.ui.eSrv.set_property(sis, None)
        
        # Port
        try:
            p = int(odApp['Port'])
            if p <= 0 or p >= 65535:
                raise ValueError
            self.ui.ePort.set_property(sis, None)
        except ValueError:
            self.ui.ePort.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        
        # User
        if odApp['User'] == '':
            self.ui.eUser.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        else:
            self.ui.eUser.set_property(sis, None)
        
        # Folder
        if odApp['Folder'] and not os.path.isdir(odApp['Folder']):
            self.ui.eFolder.set_property(sis, Gtk.STOCK_DIALOG_WARNING)
            valid = False
        else:
            self.ui.eFolder.set_property(sis, None)
        
        if not valid:
            self.ui.lStatus.set_text(_('Please check your application configuration'))
            return

        if self.ui.tsApp.count_selected_rows() == 0:
            # this is a new savefile
            odApp['Conf'] = str(int(round(time())))+'.winconn'

            self.ui.lsApps.append(odApp.values())
            self.ui.lStatus.set_text(_('New application added successfully'))
        else:
            # this is current App update
            tm, ti = self.ui.tsApp.get_selected()
            odApp['Conf'] = tm.get_value(ti, 12)
            lApp = odApp.values()
            for i in range(0, tm.get_n_columns()-1):
                self.ui.lsApps.set_value(ti, i, lApp[i])
            self.ui.lStatus.set_text(_('Application updated successfully'))
            
        # FIXME add section name
        config = ConfigParser.SafeConfigParser(odApp)
        with open(self.common.get_conf()+odApp['Conf'],'w') as cfgfile:
            config.write(cfgfile)
                
    def tsApp_changed(self, widget):
        lApp = []
        
        tm, ti = self.ui.tsApp.get_selected()
        if ti is None:
            return
        for i in range(0, tm.get_n_columns()):
            lApp.append(tm.get_value(ti, i))
        
        self.ui.eName.set_text(lApp[0])
        self.ui.eApp.set_text(lApp[1])
        self.ui.eSrv.set_text(lApp[2])
        self.ui.ePort.set_text(str(lApp[3]))
        self.ui.eUser.set_text(lApp[4])
        self.ui.ePass.set_text(lApp[5])
        self.ui.eDomain.set_text(lApp[6])
        self.ui.eFolder.set_text(lApp[7])
        self.ui.sComp.set_active(lApp[8])
        self.ui.sClip.set_active(lApp[9])
        self.ui.sSound.set_active(lApp[10])
        self.ui.sRFX.set_active(lApp[11])
        
        self.ui.notebook.set_current_page(1)
        self.ui.lStatus.set_text('')
        
    def eFolder_icon_press(self, widget, icon=None, data=None):
        response, path = prompts.choose_directory()
        if response == Gtk.ResponseType.OK:
            widget.set_text(path)
