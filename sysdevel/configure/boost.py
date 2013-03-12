#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find Boost
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

import os, platform, subprocess

from sysdevel.util import *

environment = dict()
boost_found = False


def null():
    global environment
    environment['BOOST_INCLUDE_DIR'] = ''
    environment['BOOST_LIB_DIR'] = ''
    environment['BOOST_LIBS'] = []
    environment['BOOST_LIBRARIES'] = []


def is_installed(version=None):
    global environment, boost_found
    if version is None:
        required_version = '1_33'
    else:
        required_version = version.replace('.', '_')

    base_dirs = []
    try:
        boost_root = os.environ['BOOST_ROOT']
        boost_root = boost_root.strip('"')
        if os.path.exists(os.path.join(boost_root, 'stage', 'lib')):
            base_dirs.append(os.path.join(boost_root, 'stage'))
        base_dirs.append(boost_root)
    except:
        pass
    try:
        base_dirs.append(os.environ['BOOST_LIBRARY_DIR'])
    except:
        pass
    if 'windows' in platform.system().lower():
        base_dirs.append(os.path.normpath(os.path.join('C:', os.sep, 'Boost')))
        try:
            base_dirs.append(environment['MSYS_DIR'])
        except:
            pass
    try:
        incl_dir = find_header(os.path.join('boost', 'version.hpp'),
                               base_dirs, 'boost-*')
        lib_dir, libs = find_libraries('boost', base_dirs)
        boost_version = get_header_version(os.path.join(incl_dir, 'boost',
                                                        'version.hpp'),
                                           'BOOST_LIB_VERSION')
        boost_version = boost_version.strip('"')
        if compare_versions(boost_version, required_version) == -1:
            return boost_found
        boost_found = True
    except:
        return boost_found

    environment['BOOST_INCLUDE_DIR'] = incl_dir
    environment['BOOST_LIB_DIR'] = lib_dir
    environment['BOOST_LIBS'] = libs
    environment['BOOST_LIBRARIES'] = ['boost_python', 'boost_date_time',
                                      'boost_filesystem', 'boost_graph',
                                      'boost_iostreams',
                                      'boost_prg_exec_monitor',
                                      'boost_program_options', 'boost_regex',
                                      'boost_serialization', 'boost_signals',
                                      'boost_system', 'boost_thread',
                                      'boost_unit_test_framework', 'boost_wave',
                                      'boost_wserialization',]
    return boost_found


def install(target='build', version=None):
    if not boost_found:
        if version is None:
            version = '1_44_0'
        website = ('http://prdownloads.sourceforge.net/boost/',)
        if 'windows' in platform.system().lower():
            ## assumes MinGW installed and detected
            here = os.path.abspath(os.getcwd())
            src_dir = 'boost_' + str(version)
            archive = src_dir + '.tar.bz2'
            fetch(''.join(website), archive, archive)
            unarchive(os.path.join(here, download_dir, archive), src_dir)
            os.chdir(src_dir)
            subprocess.check_call(['bootstrap.sh', 'mingw'])
            subprocess.check_call(['bjam', 'install', '--toolset=gcc',
                                   '--prefix=' + environment['MSYS_DIR']])
            os.chdir(here)
        else:
            global_install('Boost', website,
                           None,
                           'boost +python' + ''.join(get_python_version()),
                           'libboost-dev',
                           'boost-devel')
        is_installed()