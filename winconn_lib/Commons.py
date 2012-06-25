# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from gi.repository import Gtk # pylint: disable=E0611

import gettext
from gettext import gettext as _

from os import getenv
from quickly import prompts

class Commons:
    __confdir__ = ''

    def __init__(self):
        self.__confdir__ = getenv('HOME') + '/.config/winconn/'

    def get_conf(self):
        return self.__confdir__
    
    def buildCmd(self, lApp):
        #lApp = []

        #tm, ti = self.ui.tsApp.get_selected()
        #for i in range(0, tm.get_n_columns()-1):
        #    lApp.append(tm.get_value(ti, i))
            
        cmd = ['xfreerdp', '--ignore-certificate']
        # compress
        if not lApp[8]:
            cmd.append('-z')
        # RemoteFX
        if not lApp[11]:
            cmd.append('--rfx')
        # we want RemmoteApp
        cmd.append('--app')
        # port
        if lApp[3] != '3389':
            cmd.extend(['-t', lApp[3]])
        # user
        cmd.extend(['-u', lApp[4]])
        # pass
        if lApp[5] == '':
            p = prompts.Prompt('WinConn',_('Enter password for application: ')+lApp[0])
            ePass = Gtk.Entry()
            ePass.set_visibility(False)
            ePass.set_activates_default(True)
            ePass.show()
            p.content_box.pack_end(ePass, True, True, 5)
            response = p.run()
            userPass = ePass.get_text()
            p.destroy()
            if response == Gtk.ResponseType.OK:
                lApp[5] = userPass
            else:
                return None
            
        cmd.extend(['-p', lApp[5]])
        # domain
        if lApp[6] != '':
            cmd.extend(['-d', lApp[6]])
        # clipboard
        # does not work with freerdp 1.0.1
        if not lApp[9]:
            cmd.extend(['--plugin', 'cliprdr'])
        # sound
        if not lApp[10]:
            cmd.extend(['--plugin', 'rdpsnd'])
        # folder
        if lApp[7] != '':
            cmd.extend(['--plugin', 'rdpdr', '--data', 'disk:winconn:'+lApp[7], '--'])
        # app
        cmd.extend(['--app', '--plugin', 'rail.so', '--data', lApp[1]])
        # server
        cmd.extend(['--', lApp[2]])

        return cmd

