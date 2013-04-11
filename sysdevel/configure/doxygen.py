#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find Doxygen
"""
#**************************************************************************
# 
# This material was prepared by the Los Alamos National Security, LLC 
# (LANS), under Contract DE-AC52-06NA25396 with the U.S. Department of 
# Energy (DOE). All rights in the material are reserved by DOE on behalf 
# of the Government and LANS pursuant to the contract. You are authorized 
# to use the material for Government purposes but it is not to be released 
# or distributed to the public. NEITHER THE UNITED STATES NOR THE UNITED 
# STATES DEPARTMENT OF ENERGY, NOR LOS ALAMOS NATIONAL SECURITY, LLC, NOR 
# ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR 
# ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, 
# COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR 
# PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE 
# PRIVATELY OWNED RIGHTS.
# 
#**************************************************************************

import os
from sysdevel.util import *

environment = dict()
doxygen_found = False
DEBUG = False


def null():
    global environment
    environment['DOXYGEN'] = None


def is_installed(environ, version):
    global environment, doxygen_found
    set_debug(DEBUG)
    base_dirs = []
    for d in programfiles_directories():
        base_dirs.append(os.path.join(d, 'doxygen'))
    try:
        base_dirs.append(environ['MINGW_DIR'])
        base_dirs.append(environ['MSYS_DIR'])
    except:
        pass
    try:
        environment['DOXYGEN'] = find_program('doxygen', base_dirs)
        doxygen_found = True
    except Exception, e:
        if DEBUG:
            print e
    return doxygen_found


def install(environ, version, locally=True):
    if not doxygen_found:
        if version is None:
            version = '1.8.3.1'
        website = ('http://ftp.stack.nl/pub/users/dimitri/',)
        #FIXME no local install
        global_install('Doxygen', website,
                       winstaller='doxygen-' + str(version) + '-setup.exe',
                       brew='doxygen', port='doxygen',
                       deb='doxygen', rpm='doxygen')
        if not is_installed(environ, version):
            raise Exception('Doxygen installation failed.')
