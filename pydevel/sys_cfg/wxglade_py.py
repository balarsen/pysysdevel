#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find/install wxGlade
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

from pydevel.util import *

environment = dict()
wxglade_found = False


def null():
    global environment
    environment['WXGLADE_VERSION'] = None
    environment['WXGLADE_EXECUTABLE'] = None


def is_installed(version=None):
    global environment, wxglade_found
    try:
        import wxglade.common
        ver = wxglade.common.version
        if not version is None and ver < version:
            return wxglade_found
        environment['WXGLADE_VERSION'] = ver
        environment['WXGLADE_EXECUTABLE'] = find_program('wxglade')
        wxglade_found = True
    except Exception,e:
        print 'Wxglade not found: ' + str(e)
    return wxglade_found


def install(target='build', version=None):
    global environment
    if not wxglade_found:
        if version is None:
            version = '0.6.5'
        website = 'http://downloads.sourceforge.net/project/wxglade/wxglade/' + version + '/'
        archive = 'wxGlade-' + version + '.tar.gz'
        install_pypkg_locally('wxGlade-' + version, website, archive, target)
        environment['WXGLADE_VERSION'] = version
        environment['WXGLADE_EXECUTABLE'] = find_program('wxglade.py',
							 [os.path.join(target, 'python', 'wxglade')])
