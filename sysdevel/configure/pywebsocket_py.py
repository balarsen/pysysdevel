#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find/install mod_pywebsocket
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
pywebsocket_found = False


def null():
    pass


def is_installed(environ, version):
    global pywebsocket_found
    try:
        import mod_pywebsocket
        pywebsocket_found = True
    except:
        pass
    return pywebsocket_found


def install(environ, version, target='build'):
    global environment
    if not pywebsocket_found:
        website = 'http://pywebsocket.googlecode.com/files/'
        if version is None:
            version = '0.7.6'
        src_dir = 'pywebsocket-' + str(version)
        archive = 'mod_' + src_dir + '.tar.gz'
        pkg_dir = os.path.join(src_dir, 'src')
        install_pypkg_locally(src_dir, website, archive,
                              target, src_dir=pkg_dir)
        if not is_installed(environ, version):
            raise Exception('pywebsocket installation failed.')