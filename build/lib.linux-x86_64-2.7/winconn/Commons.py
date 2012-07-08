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

from gi.repository import Gtk # pylint: disable=E0611

import gettext
from gettext import gettext as _

import os
from fnmatch import fnmatch
from time import time
import ConfigParser
from collections import OrderedDict
from quickly import prompts

import logging
logger = logging.getLogger('winconn')

class Commons:
    __confdir__ = ''
    __odApp__ = None
    __wcSection__ = 'WinConn'

    def __init__(self):
        self.__confdir__ = os.getenv('HOME') + '/.config/winconn/'
        if not os.path.isdir(self.__confdir__):
            os.makedirs(self.__confdir__)

        logger.debug('Config directory: %s', self.__confdir__)


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
            ('printer', False),
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
                                val = str(config.get(self.__wcSection__, key))
                                self.__odApp__[key] = val.replace('%%', '%')
                        except ConfigParser.NoSectionError:
                            usable = False
                            break
                        except ConfigParser.NoOptionError:
                            continue
                    if usable:
                        yield self.__odApp__.values()
    
    def setApp(self):
        if self.__odApp__['conf'] == '':
            self.__odApp__['conf'] = str(int(round(time()*1000)))+'.winconn'
        config = ConfigParser.SafeConfigParser()
        config.add_section(self.__wcSection__)
        for key in self.__odApp__:
            val = str(self.__odApp__[key]).replace('%', '%%')
            config.set(self.__wcSection__, key, val)
        
        logger.debug('Write config to file: %s', self.__odApp__['conf'])
        
        with open(self.__confdir__+self.__odApp__['conf'],'w') as cfgfile:
            config.write(cfgfile)
    
    def delApp(self):
        logger.debug('Delete config file: %s', self.__confdir__+self.__odApp__['conf'])
        os.unlink(self.__confdir__+self.__odApp__['conf'])
        
    def importRemmina(self, lAppNames):
        lMap = [
            ('name', 'name'),
            ('server', 'server'),
            ('username', 'user'),
            ('domain', 'domain'),
            ('sharefolder', 'folder'),
            ('disableclipboard', 'clipboard'),
            ('sound', 'sound'),
            ('shareprinter', 'printer')
        ]
        remmconf = os.getenv('HOME') + '/.remmina/'
        remmsect = 'remmina'
        if not os.path.isdir(remmconf):
            return

        for fname in os.listdir(remmconf):
            if fnmatch(fname, '*.remmina'):
                self.init_App()
                
                logger.debug('Import from: %s', remmconf+fname)
                
                with open(remmconf+fname, 'r') as conf:
                    config = ConfigParser.SafeConfigParser()
                    config.readfp(conf)
                    if config.has_option(remmsect, 'name'):
                        lRemm = dict(config.items(remmsect))
                        if lRemm['protocol'] != 'RDP' or lRemm['name'] in lAppNames:
                            continue
                        for remm, wc in lMap:
                            if config.has_option(remmsect, remm):
                                opt = str(config.get(remmsect, remm))
                                if remm == 'server':
                                    lSrv = opt.split(':', 1)
                                    if len(lSrv) == 2:
                                        self.__odApp__[wc] = lSrv[0]
                                        self.__odApp__['port'] = lSrv[1]
                                    else:
                                        self.__odApp__[wc] = opt
                                elif remm == 'sound':
                                    if opt == 'off' or opt == 'remote':
                                        self.__odApp__[wc] = True
                                elif remm == 'shareprinter':
                                    self.__odApp__[wc] = not config.getboolean(remmsect, remm)
                                elif isinstance(self.__odApp__[wc], bool):
                                    self.__odApp__[wc] = config.getboolean(remmsect, remm)
                                else:
                                    self.__odApp__[wc] = opt

                        logger.debug('Imported values: %s', self.__odApp__)

                        yield self.__odApp__.values()

    def importRDP(self, lAppNames, rdpfile):
        lMap = dict([
            ('remoteapplicationname', 'name'),
            ('remoteapplicationprogram', 'app'),
            ('full address', 'server'),
            ('server port', 'port'),
            ('username', 'user'),
            ('compression', 'compress'),
            ('redirectclipboard', 'clipboard'),
            ('audiomode', 'sound'),
            ('redirectprinters', 'printer'),
            ('redirectdirectx', 'remotefx')
        ])
        
        logger.debug('Import RDP file: %s', rdpfile)
        
        with open(rdpfile, 'r') as frdp:
            self.init_App()
            lrdp = frdp.readlines()
            
        for opt in lrdp:
            ll = opt.split(':', 2)
            if len(ll) != 3:
                continue
            ll[2] = ll[2].replace("\n", '')

            if  lMap.has_key(ll[0]):
                if lMap[ll[0]] in ('compress', 'clipboard', 'printer', 'remotefx'):
                    if ll[2] == '1':
                        self.__odApp__[lMap[ll[0]]] = False
                    else:
                        self.__odApp__[lMap[ll[0]]] = True
                elif lMap[ll[0]] == 'sound':
                    if ll[2] == '0':
                        self.__odApp__[lMap[ll[0]]] = False
                    else:
                        self.__odApp__[lMap[ll[0]]] = True
                else:
                    self.__odApp__[lMap[ll[0]]] = ll[2]

        if self.__odApp__['server'] == '':
            return False

        if self.__odApp__['name'] == '':
            self.__odApp__['name'] = os.path.basename(rdpfile)
            
        if self.__odApp__['name'] in lAppNames:
            return False
        
        logger.debug('Imported values: %s', self.__odApp__)
        
        return True
    
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
        # printer
        if not self.__odApp__['printer']:
            cmd.extend(['--plugin', 'rdpdr', '--data', 'printer'])
        # folder
        if self.__odApp__['folder'] != '':
            cmd.extend(['--plugin', 'rdpdr', '--data', 'disk:winconn:{0}'.format(self.__odApp__['folder'])])
        # --
        if not self.__odApp__['printer'] or self.__odApp__['folder'] != '':
            cmd.append('--')
        # app
        cmd.extend(['--app', '--plugin', 'rail.so', '--data', self.__odApp__['app'], '--'])
        # server
        cmd.append(self.__odApp__['server'])
        
        logger.debug(cmd)

        return cmd
