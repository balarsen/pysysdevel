"""
'build_src' command, adding module generation using ANTLR grammars
"""

import os
import sys
import shutil
import glob
import subprocess

try:
    from numpy.distutils.command.build_src import build_src as _build_src
except:
    from distutils.command.build_src import build_src as _build_src

import util


class build_src(_build_src):
    '''
    Build python modules from ANTLR grammars
    '''
    def initialize_options(self):
        _build_src.initialize_options(self)
        self.devel_support = []
        self.antlr_modules = []

    def finalize_options(self):
        _build_src.finalize_options(self)
        self.devel_support = self.distribution.devel_support
        self.antlr_modules = self.distribution.antlr_modules
  

    def run(self):
        environ = self.distribution.environment

        if self.devel_support:
            for tpl in self.devel_support:
                if self.distribution.verbose:
                    print 'adding sysdevel support to ' + tpl[0]
                target = os.path.abspath(os.path.join(self.build_lib,
                                                      *tpl[0].split('.')))
                util.mkdir(target)
                source_dir = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), 'support'))
                for mod in tpl[1]:
                    src_file = os.path.join(source_dir, mod + '.py.in')
                    if not os.path.exists(src_file):
                        src_file = src_file[:-3]
                    dst_file = os.path.join(target, mod + '.py')
                    util.configure_file(environ, src_file, dst_file)


        if self.antlr_modules:
            here = os.getcwd()
            for grammar in self.antlr_modules:
                if self.distribution.verbose:
                    print 'building antlr grammar "' + \
                        grammar.name + '" sources'
                ##TODO build in build_src, add to build_lib modules
                target = os.path.abspath(os.path.join(self.build_lib,
                                                      grammar.directory))
                util.mkdir(target)
                source_dir = os.path.abspath(grammar.directory)
                os.chdir(target)

                reprocess = True
                ref = os.path.join(target, grammar.name + '2Py.py')
                if os.path.exists(ref):
                    reprocess = False
                    for src in grammar.sources:
                        src_path = os.path.join(source_dir, src)
                        if os.path.getmtime(ref) < os.path.getmtime(src_path):
                            reprocess = True
                if reprocess:
                    for src in grammar.sources:
                        ## ANTLR cannot parse from a separate directory
                        shutil.copy(os.path.join(source_dir, src), '.')
                        cmd_line = list(environ['ANTLR'])
                        cmd_line.append(src)
                        status = subprocess.call(cmd_line)
                        if status != 0:
                            raise Exception("Command '" + str(cmd_line) +
                                            "' returned non-zero exit status "
                                            + str(status))
                    ## Cleanup so that it's only Python modules
                    for f in glob.glob('*.g'):
                        os.unlink(f)
                    for f in glob.glob('*.tokens'):
                        os.unlink(f)
                os.chdir(here)
        _build_src.run(self)
