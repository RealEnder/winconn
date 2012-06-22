#!/usr/bin/python
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

import unittest
import subprocess

class TestPylint(unittest.TestCase):
    def test_project_errors_only(self):
        '''run pylint in error only mode
        
        your code may well work even with pylint errors
        but have some unusual code'''
        return_code = subprocess.call(["pylint", '-E', 'winconn'])
        # not needed because nosetests displays pylint console output
        #self.assertEqual(return_code, 0)

    # un-comment the following for loads of diagnostics   
    #~ def test_project_full_report(self):
        #~ '''Only for the brave
#~ 
        #~ you will have to make judgement calls about your code standards
        #~ that differ from the norm'''
        #~ return_code = subprocess.call(["pylint", 'winconn'])

if __name__ == '__main__':
    'you will get better results with nosetests'
    unittest.main()
