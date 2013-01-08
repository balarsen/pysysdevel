#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find/install Py++/PyGCCXML
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
pyplusplus_found = False


def null():
    global environment
    environment['PYPLUSPLUS_VERSION'] = None


def is_installed(version=None):
    global environment, pyplusplus_found
    try:
        import pyplusplus
        try:
            environment['PYPLUSPLUS_VERSION'] = pyplusplus.__version__
        except:
            pass
        pyplusplus_found = True
    except Exception,e:
        print 'Py++ not found: ' + str(e)
    return pyplusplus_found


def install(target='build', version=None):
    global environment
    if not pyplusplus_found:
        if version is None:
            version = '1.0.0'
        website = 'http://downloads.sourceforge.net/project/pygccxml/pygccxml/pygccxml-' + version[:-2] + '/'
        archive = 'pygccxml-' + version + '.zip'
        install_pypkg_locally('pygccxml-' + version, website, archive, target)

        website = 'http://downloads.sourceforge.net/project/pygccxml/pyplusplus/pyplusplus-' + version[:-2] + '/'
        archive = 'pyplusplus-' + version + '.zip'
        install_pypkg_locally('pyplusplus-' + version, website, archive, target)
        environment['PYPLUSPLUS_VERSIONSION'] = version