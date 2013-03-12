#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find/install Euclid
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

from sysdevel.util import *

environment = dict()
euclid_found = False


def null():
    pass


def is_installed(version=None):
    global environment, euclid_found
    try:
        import euclid
        ver = euclid.__revision__.split()[1]
        if not version is None and ver < version:
            return euclid_found
        euclid_found = True
    except Exception,e:
        pass
    return euclid_found


def install(target='build', version=None):
    if not euclid_found:
        website = 'https://pypi.python.org/packages/source/e/euclid/'
        if version is None:
            version = '0.01'
        archive ='euclid-' + str(version) + '.tar.gz' 
        install_pypkg_locally('euclid-' + str(version), website, archive, target)
