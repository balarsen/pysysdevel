"""
Custom setup
"""

import sys
import sysdevel
if sysdevel.using_setuptools and sys.version_info > (2, 5):
    ## setuptools is broken in at least Python 2.4
    try:
        ## Must be first (get the monkeypatching out of the way)
        import setuptools
    except:
        pass

import shutil
import os
import platform
import subprocess
import glob

have_numpy = False
try:
    from numpy.distutils.numpy_distribution import NumpyDistribution as oldDistribution
    from numpy.distutils.command import config, build_ext, install_headers
    from numpy.distutils.command import bdist_rpm, scons
    have_numpy = True

except ImportError, e:
    print 'NumPy not found. Failover to distutils alone.'
    from distutils.dist import Distribution as oldDistribution
    from distutils.command import config, build_ext, install_headers, bdist_rpm

import util



class CustomDistribution(oldDistribution):
    '''
    Subclass Distribution to support new commands
    '''
    def __init__(self, attrs=None):
        old_attrs = attrs
        ## setup the environment for custom commands
        self.environment = attrs.get('environment')
        if self.environment != None:
            del old_attrs['environment']
        else:
            self.environment = dict()
        ## PYJS web extensions
        self.web_ext_modules = attrs.get('web_ext_modules')
        if self.web_ext_modules != None:
            del old_attrs['web_ext_modules']
        ## Sphinx documentation
        self.doc_modules = attrs.get('doc_modules')
        if self.doc_modules != None:
            del old_attrs['doc_modules']
        ## Py++ extensions
        self.pypp_ext_modules = attrs.get('pypp_ext_modules')
        if self.pypp_ext_modules != None:
            del old_attrs['pypp_ext_modules']
        ## Shared libraries
        self.sh_libraries = attrs.get('sh_libraries')
        if self.sh_libraries != None:
            del old_attrs['sh_libraries']
        ## ANTLR parser/lexers
        self.antlr_modules = attrs.get('antlr_modules')
        if self.antlr_modules != None:
            del old_attrs['antlr_modules']
        ## Native executables
        self.native_executables = attrs.get('native_executables')
        if self.native_executables != None:
            del old_attrs['native_executables']
        ## Data to install to 'share'
        self.data_dirs = attrs.get('data_dirs')
        if self.data_dirs != None:
            del old_attrs['data_dirs']
        ## Non-stock libraries to install to 'lib' or 'lib64'
        self.extra_install_libraries = attrs.get('extra_install_libraries')
        if self.extra_install_libraries != None:
            del old_attrs['extra_install_libraries']
        ## Non-stock python packages to co-install
        self.extra_install_modules = attrs.get('extra_install_modules')
        if self.extra_install_modules != None:
            del old_attrs['extra_install_modules']
        ## Boilerplate scripts to create
        self.create_scripts = attrs.get('create_scripts')
        if self.create_scripts != None:
            del old_attrs['create_scripts']
        ## SysDevel support modules
        self.devel_support = attrs.get('devel_support')
        if self.devel_support != None:
            del old_attrs['devel_support']
        ## Files to delete upon 'clean'
        self.generated_files = attrs.get('generated_files')
        if self.generated_files != None:
            del old_attrs['generated_files']
        ## Separate packages with their own setup.py
        self.subpackages = attrs.get('subpackages')
        if self.subpackages != None:
            del old_attrs['subpackages']
        ## Whether to quit if a subpackage build fails
        self.quit_on_error = attrs.get('quit_on_error')
        if self.quit_on_error != None:
            del old_attrs['quit_on_error']
        else:
            self.quit_on_error = True
        ## Enable parallel building
        self.parallel_build = attrs.get('parallel_build')
        if self.parallel_build != None:
            del old_attrs['parallel_build']
        ## Unit testing
        self.tests = attrs.get('tests')
        if self.tests != None:
            del old_attrs['tests']


        ## py2exe options
        self.ctypes_com_server = attrs.pop("ctypes_com_server", [])
        self.com_server = attrs.pop("com_server", [])
        self.service = attrs.pop("service", [])
        self.windows = attrs.pop("windows", [])
        self.console = attrs.pop("console", [])
        self.isapi = attrs.pop("isapi", [])
        self.zipfile = attrs.pop("zipfile", util.default_py2exe_library)

        oldDistribution.__init__(self, old_attrs)

    def has_scripts(self):
        return oldDistribution.has_scripts(self) or \
            (self.create_scripts != None and len(self.create_scripts) > 0)

    def has_c_libraries(self):
        return oldDistribution.has_c_libraries(self) or self.has_shared_libs()

    def has_shared_libs(self):
        return (self.sh_libraries != None and len(self.sh_libraries) > 0) or \
            (self.extra_install_libraries != None and
             len(self.extra_install_libraries) > 0)

    def has_antlr_extensions(self):
        return self.antlr_modules != None and len(self.antlr_modules) > 0

    def has_sysdevel_support(self):
        return self.devel_support != None and len(self.devel_support) > 0

    def has_pypp_extensions(self):
        return self.pypp_ext_modules != None and \
            len(self.pypp_ext_modules) > 0

    def has_web_extensions(self):
        return self.web_ext_modules != None and len(self.web_ext_modules) > 0

    def has_documents(self):
        return self.doc_modules != None and len(self.doc_modules) > 0

    def has_executables(self):
        return self.native_executables != None and \
            len(self.native_executables) > 0

    def has_data_directories(self):
        return self.data_dirs != None and len(self.data_dirs) > 0



##################################################
## Almost verbatim from numpy.disutils.core
##################################################

if 'setuptools' in sys.modules:
    have_setuptools = True
    from setuptools import setup as old_setup
    # easy_install imports math, it may be picked up from cwd
    from setuptools.command import easy_install
    try:
        # very old versions of setuptools don't have this
        from setuptools.command import bdist_egg
    except ImportError:
        have_setuptools = False
else:
    from distutils.core import setup as old_setup
    have_setuptools = False

allows_py2app = False
try:
    from py2app.build_app import py2app
    allows_py2app = True
except:
    pass


import warnings
import distutils.core
import distutils.dist

import config_cc
import config_fc
import build
import build_doc
import build_js
import build_py
import build_scripts
import build_pypp_ext
import build_src
import build_clib
import build_shlib
import build_exe
import sdist
import install
import install_data
import install_lib
import install_clib
import install_exe
import clean
import test

my_cmdclass = {'build':            build.build,
               'build_src':        build_src.build_src,
               'build_scripts':    build_scripts.build_scripts,
               'config_cc':        config_cc.config_cc,
               'config_fc':        config_fc.config_fc,
               'config':           config.config,
               'build_ext':        build_ext.build_ext,
               'build_py':         build_py.build_py,
               'build_clib':       build_clib.build_clib,
               'build_shlib':      build_shlib.build_shlib,
               'build_js':         build_js.build_js,
               'build_doc':        build_doc.build_doc,
               'build_pypp_ext':   build_pypp_ext.build_pypp_ext,
               'build_exe':        build_exe.build_exe,
               'sdist':            sdist,
               'install_exe':      install_exe.install_exe,
               'install_lib':      install_lib.install_lib,
               'install_clib':     install_clib.install_clib,
               'install_data':     install_data.install_data,
               'install_headers':  install_headers.install_headers,
               'install':          install.install,
               'bdist_rpm':        bdist_rpm.bdist_rpm,
               'clean':            clean.clean,
               'test':             test.test,
               }

if have_numpy:
    my_cmdclass['scons']         = scons.scons

if have_setuptools:
    if have_numpy:
        # Use our own versions of develop and egg_info to ensure that build_src
        # is handled appropriately.
        from numpy.distutils.command import develop, egg_info
        
    my_cmdclass['bdist_egg']     = bdist_egg.bdist_egg
    if have_numpy:
        my_cmdclass['develop']   = develop.develop
    my_cmdclass['easy_install']  = easy_install.easy_install
    if have_numpy:
        my_cmdclass['egg_info']  = egg_info.egg_info
    
if allows_py2app:
    my_cmdclass['py2app']        = py2app


def _dict_append(d, **kws):
    for k,v in kws.items():
        if k not in d:
            d[k] = v
            continue
        dv = d[k]
        if isinstance(dv, tuple):
            d[k] = dv + tuple(v)
        elif isinstance(dv, list):
            d[k] = dv + list(v)
        elif isinstance(dv, dict):
            _dict_append(dv, **v)
        elif util.is_string(dv):
            d[k] = dv + v
        else:
            raise TypeError, repr(type(dv))

def _command_line_ok(_cache=[]):
    """ Return True if command line does not contain any
    help or display requests.
    """
    if _cache:
        return _cache[0]
    ok = True
    display_opts = ['--'+n for n in distutils.dist.Distribution.display_option_names]
    for o in distutils.dist.Distribution.display_options:
        if o[1]:
            display_opts.append('-'+o[1])
    for arg in sys.argv:
        if arg.startswith('--help') or arg=='-h' or arg in display_opts:
            ok = False
            break
    _cache.append(ok)
    return ok


def get_distribution(always=False):
    dist = distutils.core._setup_distribution
    # XXX Hack to get numpy installable with easy_install.
    # The problem is easy_install runs it's own setup(), which
    # sets up distutils.core._setup_distribution. However,
    # when our setup() runs, that gets overwritten and lost.
    # We can't use isinstance, as the DistributionWithoutHelpCommands
    # class is local to a function in setuptools.command.easy_install
    if dist is not None and \
            'DistributionWithoutHelpCommands' in repr(dist):
        dist = None
    if always and dist is None:
        dist = CustomDistribution()
    return dist


def setup(**attr):
    if len(sys.argv)<=1 and not attr.get('script_args',[]):
        try:
            from numpy.distutils.interactive import interactive_sys_argv
            from numpy.distutils.core import _exit_interactive_session
            import atexit
            atexit.register(_exit_interactive_session)
            sys.argv[:] = interactive_sys_argv(sys.argv)
            if len(sys.argv)>1:
                return setup(**attr)
        except:
            pass

    cmdclass = my_cmdclass.copy()

    new_attr = attr.copy()
    if 'cmdclass' in new_attr:
        cmdclass.update(new_attr['cmdclass'])
    new_attr['cmdclass'] = cmdclass

    if 'configuration' in new_attr:
        # To avoid calling configuration if there are any errors
        # or help request in command in the line.
        configuration = new_attr.pop('configuration')

        old_dist = distutils.core._setup_distribution
        old_stop = distutils.core._setup_stop_after
        distutils.core._setup_distribution = None
        distutils.core._setup_stop_after = "commandline"
        try:
            dist = setup(**new_attr)
        finally:
            distutils.core._setup_distribution = old_dist
            distutils.core._setup_stop_after = old_stop
        if dist.help or not _command_line_ok():
            # probably displayed help, skip running any commands
            return dist

        # create setup dictionary and append to new_attr
        config = configuration()
        if hasattr(config,'todict'):
            config = config.todict()
        _dict_append(new_attr, **config)

    # Move extension source libraries to libraries
    libraries = []
    for ext in new_attr.get('ext_modules',[]):
        new_libraries = []
        for item in ext.libraries:
            #[item] = util.convert_ulist([item])
            if util.is_sequence(item):
                lib_name, build_info = item
                _check_append_ext_library(libraries, item)
                new_libraries.append(lib_name)
            elif util.is_string(item):
                new_libraries.append(item)
            else:
                raise TypeError("invalid description of extension module "
                                "library %r" % (item,))
        ext.libraries = new_libraries
    if libraries:
        if 'libraries' not in new_attr:
            new_attr['libraries'] = []
        for item in libraries:
            _check_append_library(new_attr['libraries'], item)

    # sources in ext_modules or libraries may contain header files
    if ('ext_modules' in new_attr or 'libraries' in new_attr) \
       and 'headers' not in new_attr:
        new_attr['headers'] = []

    # Use our custom Distribution class instead of distutils' one
    new_attr['distclass'] = CustomDistribution

    return old_setup(**new_attr)


def _check_append_library(libraries, item):
    for libitem in libraries:
        if util.is_sequence(libitem):
            if util.is_sequence(item):
                if item[0]==libitem[0]:
                    if item[1] is libitem[1]:
                        return
                    warnings.warn("[0] libraries list contains %r with"
                                  " different build_info" % (item[0],))
                    break
            else:
                if item==libitem[0]:
                    warnings.warn("[1] libraries list contains %r with"
                                  " no build_info" % (item[0],))
                    break
        else:
            if util.is_sequence(item):
                if item[0]==libitem:
                    warnings.warn("[2] libraries list contains %r with"
                                  " no build_info" % (item[0],))
                    break
            else:
                if item==libitem:
                    return
    libraries.append(item)

def _check_append_ext_library(libraries, (lib_name,build_info)):
    for item in libraries:
        if util.is_sequence(item):
            if item[0]==lib_name:
                if item[1] is build_info:
                    return
                warnings.warn("[3] libraries list contains %r with"
                              " different build_info" % (lib_name,))
                break
        elif item==lib_name:
            warnings.warn("[4] libraries list contains %r with"
                          " no build_info" % (lib_name,))
            break
    libraries.append((lib_name,build_info))
