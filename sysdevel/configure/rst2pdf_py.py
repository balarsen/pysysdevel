
from sysdevel.util import *
from sysdevel.configuration import py_config

class configuration(py_config):
    """
    Find/install rst2pdf
    """
    def __init__(self):
        py_config.__init__(self, 'rst2pdf', '0.93',
                           dependencies=['docutils', 'reportlab',
                                         'pygments', 'pdfrw'],
                           debug=False)


    def install(self, environ, version, locally=True):
        if not self.found:
            website = 'http://rst2pdf.googlecode.com/files/'
            if version is None:
                version = self.version
            src_dir = 'rst2pdf-' + str(version)
            archive = src_dir + '.tar.gz' 
            install_pypkg(src_dir, website, archive, locally=locally)
            if not self.is_installed(environ, version):
                raise Exception('rst2pdf installation failed.')
