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

from collections import OrderedDict
from time import time

import os
import os.path
from fnmatch import fnmatch
import ConfigParser

# See winconn_lib.Window.py for more details about how this class works
class WinconnWindow(Window):
    __gtype_name__ = 'WinconnWindow'
    confdir = ''
    
    def emptyApp(self):
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
    
    def readApps(self):
        for fname in os.listdir(self.confdir):
            if fnmatch(fname, '*.winconn'):
                with open(self.confdir+fname, 'r') as conf:
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
        
        self.confdir = os.getenv('HOME') + '/.winconn/'
        self.readApps()



    def tbNew_clicked_cb(self, widget):
        self.emptyApp()
        self.set_focus(self.ui.eName)
        self.ui.notebook.set_current_page(1)
        
    def tbExec_clicked_cb(self, widget, data=None):
        if self.ui.tsApp.count_selected_rows() == 0:
            self.ui.lStatus.set_text(_('No application selected'))

    def bCancel_clicked(self, widget):
        self.ui.notebook.set_current_page(0)
        self.emptyApp()

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
        odApp['Compress'] = self.ui.cbComp.get_active()
        odApp['Clipboad'] = self.ui.cbClip.get_active()
        odApp['Sound'] = self.ui.cbSound.get_active()
        odApp['RemoteFX'] = self.ui.cbRFX.get_active()
           
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
            odApp['Port'] = int(odApp['Port'])
            if odApp['Port'] <= 0 or odApp['Port'] >= 65535:
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
        
        # everyting OK, proceeed with save
        if not os.path.isdir(self.confdir):
            os.makedirs(self.confdir)

        if self.ui.tsApp.count_selected_rows() == 0:
            # this is a new savefile
            odApp['Conf'] = str(int(round(time())))+'.winconn'
            # FIXME add section name
            config = ConfigParser.SafeConfigParser(odApp)
            with open(self.confdir+odApp['Conf'],'w') as cfgfile:
                config.write(cfgfile)

            self.ui.lsApps.append(odApp.values())
            
    def tsApp_changed(self, widget):
        tm, tl = widget.get_selected_rows()
        print(tl)
        
