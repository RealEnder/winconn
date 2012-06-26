# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
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
### END LICENSE

from gi.repository import Gtk # pylint: disable=E0611

import gettext
from gettext import gettext as _

import os
from fnmatch import fnmatch
import ConfigParser
from collections import OrderedDict
from quickly import prompts

class Commons:
    __confdir__ = ''
    __odApp__ = None
    __wcSection__ = 'WinConn'

    def __init__(self):
        self.__confdir__ = os.getenv('HOME') + '/.config/winconn/'
        if not os.path.isdir(self.__confdir__):
            os.makedirs(self.__confdir__)
        

    def get_conf(self):
        return self.__confdir__
    
    def init_App(self):
        self.__odApp__ = OrderedDict([
            ('name', ''),
            ('app', ''),
            ('server', ''),
            ('port', '3389'),
            ('user', ''),
            ('pass', ''),
            ('domain', ''),
            ('folder', ''),
            ('compress', False),
            ('clipboard', True),
            ('sound', False),
            ('remotefx', False),
            ('conf', '')
        ])
    
    def get_App_opt(self, opt=None):
        if opt is None:
            return self.__odApp__.values()
        else:
            try:
                if isinstance(opt, int):
                    return self.__odApp__.values()[opt]
                else:
                    return self.__odApp__[opt]
            except KeyError:
                return None

    def set_App_opt(self, opt, val):
        try:
            if isinstance(opt, int):
                self.__odApp__[self.__odApp__.keys()[opt]] = val
            else:
                self.__odApp__[opt] = val
        except KeyError:
            pass

    def getApp(self, singlefname='*.winconn'):
        for fname in os.listdir(self.__confdir__):
            if fnmatch(fname, singlefname):
                self.init_App()
                with open(self.__confdir__+fname, 'r') as conf:
                    config = ConfigParser.SafeConfigParser()
                    config.readfp(conf)
                    for key in self.__odApp__:
                        usable = True
                        try:
                            if isinstance(self.__odApp__[key], bool):
                                self.__odApp__[key] = config.getboolean(self.__wcSection__, key)
                            else:
                                self.__odApp__[key] = config.get(self.__wcSection__, key)
                        except ConfigParser.NoSectionError:
                            usable = False
                            break
                        except ConfigParser.NoOptionError:
                            continue
                    if usable:
                        yield self.__odApp__.values()
    
    def setApp(self):
        config = ConfigParser.SafeConfigParser()
        config.add_section(self.__wcSection__)
        for key in self.__odApp__:
            config.set(self.__wcSection__, key, str(self.__odApp__[key]))
        
        with open(self.__confdir__+self.__odApp__['conf'],'w') as cfgfile:
            config.write(cfgfile)
    
    def delApp(self):
        os.unlink(self.__confdir__+self.__odApp__['conf'])

    def buildCmd(self):
        cmd = ['xfreerdp', '--ignore-certificate']
        # compress
        if not self.__odApp__['compress']:
            cmd.append('-z')
        # RemoteFX
        if not self.__odApp__['remotefx']:
            cmd.append('--rfx')

        # port
        if self.__odApp__['port'] != '3389':
            cmd.extend(['-t', self.__odApp__['port']])
        # user
        cmd.extend(['-u', self.__odApp__['user']])
        # pass
        if self.__odApp__['pass'] == '':
            p = prompts.Prompt('WinConn',_('Enter password for application: ')+self.__odApp__['name'])
            ePass = Gtk.Entry()
            ePass.set_visibility(False)
            ePass.set_activates_default(True)
            ePass.show()
            p.content_box.pack_end(ePass, True, True, 5)
            response = p.run()
            userPass = ePass.get_text()
            p.destroy()
            if response == Gtk.ResponseType.OK:
                self.__odApp__['pass'] = userPass
            else:
                return None
            
        cmd.extend(['-p', self.__odApp__['pass']])
        # domain
        if self.__odApp__['domain'] != '':
            cmd.extend(['-d', self.__odApp__['domain']])
        # clipboard
        # does not work with freerdp 1.0.1
        if not self.__odApp__['clipboard']:
            cmd.extend(['--plugin', 'cliprdr'])
        # sound
        if not self.__odApp__['sound']:
            cmd.extend(['--plugin', 'rdpsnd'])
        # folder
        if self.__odApp__['folder'] != '':
            cmd.extend(['--plugin', 'rdpdr', '--data', 'disk:winconn:'+self.__odApp__['folder'], '--'])
        # app
        cmd.extend(['--app', '--plugin', 'rail.so', '--data', self.__odApp__['app']])
        # server
        cmd.extend(['--', self.__odApp__['server']])

        return cmd
