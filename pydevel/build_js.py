# -*- coding: utf-8 -*-
"""
'build_js' command for python-to-javascript conversion using Pyjamas
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

import os, sys, logging, subprocess
from numpy.distutils.command.build_ext import build_ext
from distutils.errors import DistutilsExecError

import util


class build_js(build_ext):
    '''
    Build Pyjamas web interfaces using WebExtension
    '''
    user_options = build_ext.user_options + [
        ('pyjscompiler=', None,
         "specify the Pyjamas python-to-javascript compiler path"),
        ('pyjspath=', None,
         "specify the path to the Pyjamas distribution"),
        ]

    def initialize_options(self):
        build_ext.initialize_options(self)
        self.web_ext_modules = []
        self.pyjscompiler = None
        self.pyjspath = None

    def finalize_options(self):
        build_ext.finalize_options(self)
        self.web_ext_modules = self.distribution.web_ext_modules
        if self.pyjspath is None:
            try:
                import pyjs
                self.pyjspath = os.path.dirname(pyjs.__file__)
            except:
                pass
        else:
            sys.path.insert(0, os.path.join(self.pyjspath, 'build', 'lib'))
        if self.pyjscompiler is None:
            try:
                self.pyjscompiler = util.find_program('pyjsbuild',
                                                      [self.pyjspath])
            except:
                pass


    def run(self):
        if not self.web_ext_modules:
            return

        ## Make sure that extension sources are complete.
        self.run_command('build_src')
        build = self.get_finalized_command('build')
        environ = self.distribution.environment

        import pyjs
        ## TODO: use pyjs module directly (instead of 'pyjsbuild')
        for wext in self.web_ext_modules:
            if self.distribution.verbose:
                print 'building web extension "' + \
                    os.path.join(wext.public_subdir, wext.name) + '" sources'

            target = os.path.abspath(os.path.join(build.build_base, 'http',
                                                  wext.public_subdir))
            util.mkdir(target)
            here = os.getcwd()
            src_dir = os.path.abspath(wext.source_directory)
            working_dir = os.path.abspath(os.path.join(build.build_temp,
                                                       'web', wext.name))
            util.mkdir(working_dir)

            reprocess = True
            ref = os.path.join(target, wext.name + '.html')
            if os.path.exists(ref) and not self.force:
                reprocess = False
                for src in wext.sources:
                    if os.path.getmtime(ref) < os.path.getmtime(src):
                        reprocess = True
            if reprocess:
                for s in wext.sources:
                    util.configure_file(environ, s,
                                        os.path.join(working_dir,
                                                     os.path.basename(s)))
                ## Specifying public-folder is broken (see below)
                util.copy_tree(os.path.join(src_dir, 'public'),
                               os.path.join(working_dir, 'public'),
                               update=True, verbose=self.distribution.verbose,
                               excludes=['.svn', 'CVS'])

                compiler = wext.compiler or \
                    environ['PYJSBUILD_EXECUTABLE'] or \
                    self.pyjscompiler
                if compiler is None:
                    raise DistutilsExecError, \
                        "no value pyjsbuild executable found or given"
                cmd_line = [os.path.abspath(compiler)]
                for arg in wext.extra_compile_args:
                    if 'debug' in arg.lower():
                        cmd_line.append('--debug')
                        cmd_line.append('--print-statements')
                if self.distribution.verbose:
                    cmd_line.append('--log-level=' + str(logging.INFO))
                else:
                    cmd_line.append('--log-level=' + str(logging.ERROR))
                cmd_line.append('--output=' + target)
                ## RuntimeError: File not found '_pyjs.js' (bypassed above)
                #cmd_line.append('--public-folder=' +
                #                os.path.join(src_dir, 'public'))
                cmd_line.append(wext.name)

                os.chdir(working_dir)
                print "Running cmd_line"
                status = subprocess.call(cmd_line)
                if status != 0:
                    raise Exception("Command '" + str(cmd_line) +
                                    "' returned non-zero exit status "
                                    + str(status))
                os.chdir(here)
            if not os.path.lexists(os.path.join(target, 'index.html')):
                os.chdir(target)
                os.symlink(wext.name + '.html', 'index.html')
                os.chdir(here)