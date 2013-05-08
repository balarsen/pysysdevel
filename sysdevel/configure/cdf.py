#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find NASA Common Data Format library
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
import platform
import subprocess

from sysdevel.util import *

if 'windows' in platform.system().lower():
    DEPENDENCIES = ['mingw']

environment = dict()
cdf_found = False
DEBUG = False


def null():
    global environment
    environment['CDF_INCLUDE_DIR'] = None
    environment['CDF_LIB_DIR'] = None
    environment['CDF_LIBS'] = []
    environment['CDF_LIBRARIES'] = []


def is_installed(environ, version):
    global environment, cdf_found
    set_debug(DEBUG)
    lib_name = 'cdf'
    if 'windows' in platform.system().lower():
        lib_name += 'NativeLibrary'
    base_dirs = []
    if 'windows' in platform.system().lower():
        base_dirs.append(os.path.join('C:', os.sep, 'CDF Distribution',
                                      'cdf' + version + '-dist'))
    try:
        base_dirs.append(environ['MINGW_DIR'])
        base_dirs.append(environ['MSYS_DIR'])
    except:
        pass
    try:
        incl_dir = find_header('cdf.h', base_dirs)
        lib_dir, lib = find_library('cdf', base_dirs)
        cdf_found = True
    except Exception, e:
        if DEBUG:
            print e
        return cdf_found

    environment['CDF_INCLUDE_DIR'] = incl_dir
    environment['CDF_LIB_DIR'] = lib_dir
    environment['CDF_LIBS'] = [lib]
    environment['CDF_LIBRARIES'] = [lib_name]
    return cdf_found


def install(environ, version, locally=True):
    global local_search_paths
    if not cdf_found:
        if version is None:
            version = '34_1'
        website = ('http://cdf.gsfc.nasa.gov/',)
        if locally or not 'darwin' in platform.system().lower():
            here = os.path.abspath(os.getcwd())
            if locally:
                prefix = os.path.abspath(target_build_dir)
                if not prefix in local_search_paths:
                    local_search_paths.append(prefix)
            else:
                prefix = global_prefix
            prefix = convert2unixpath(prefix)  ## MinGW shell strips backslashes

            website = ('http://cdaweb.gsfc.nasa.gov/',
                       'pub/software/cdf/dist/cdf' + str(version))
            oper_sys = os_dir = 'linux'
            if 'windows' in platform.system().lower():
                os_dir = 'windows/src_distribution'
                oper_sys = 'mingw'
            elif 'darwin' in platform.system().lower():
                oper_sys = 'macosx'
                os_dir = 'macosX/src_distribution'

            web_subdir = '/' + os_dir + '/'
            src_dir = 'cdf' + str(version) + '-dist'
            archive = src_dir + '-cdf.tar.gz'
            fetch(''.join(website) + web_subdir, archive, archive)
            unarchive(archive, src_dir)

            build_dir = os.path.join(target_build_dir, src_dir)
            os.chdir(build_dir)
            log = open('build.log', 'w')
            if 'windows' in platform.system().lower():
                mingw_check_call(environ, ['make',
                                           'OS=mingw', 'ENV=gnu', 'all'],
                                 stdout=log, stderr=log)
                mingw_check_call(environ, ['make',
                                           'INSTALLDIR=' + prefix, 'install'],
                                 stdout=log, stderr=log)
            else:
                check_call(['make', 'OS=' + oper_sys, 'ENV=gnu', 'all'],
                           stdout=log, stderr=log)
                if locally:
                    check_call(['make', 'INSTALLDIR=' + prefix, 'install'],
                               stdout=log, stderr=log)
                else:
                    admin_check_call(['make', 'INSTALLDIR=' + prefix,
                                      'install'], stdout=log, stderr=log)
            log.close()
            os.chdir(here)
        else:
            global_install('CDF', website, brew='cdf', port='cdf')
        if not is_installed(environ, version):
            raise Exception('CDF installation failed.')
