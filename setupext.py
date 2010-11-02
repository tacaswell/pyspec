import os
import ConfigParser
import numpy as np
import copy
from distutils.core import Extension

__version__   = "$Revision$"
__author__    = "Stuart B. Wilkins <stuwilkins@mac.com>"
__date__      = "$LastChangedDate$"
__id__        = "$Id$"

options = {'build_levmar'    : False ,
           'build_ctrans'   : False ,
           'build_princeton' : False ,
           'build_sginfo'    : False }

ext_default  = {'include_dirs' : [np.get_include()],
                'library_dirs' : [],
                'libraries'    : [] }

def parseExtensionSetup(name, config, default):
    default = copy.deepcopy(default)
    try: default['include_dirs'] = config.get(name, "include_dirs").split(os.pathsep)
    except: pass
    try: default['library_dirs'] = config.get(name, "library_dirs").split(os.pathsep)
    except: pass
    try: default['libraries'] = config.get(name, "libraries").split(",")
    except: pass

    return default
    
if os.path.exists("setup.cfg"):
    config = ConfigParser.SafeConfigParser()
    config.read("setup.cfg")

    try: options['build_levmar'] = config.getboolean("levmar","build")
    except: pass
    try: options['build_ctrans'] = config.getboolean("ctrans","build")
    except: pass
    try: options['build_princeton'] = config.getboolean("princeton","build")
    except: pass
    try: options['build_sginfo'] = config.getboolean("sginfo","build")
    except: pass

    levmar = parseExtensionSetup('levmar', config, ext_default)
    levmar['libraries'].append('levmar')

    ctrans = parseExtensionSetup('ctrans', config, ext_default)
    princeton = parseExtensionSetup('princeton', config, ext_default)
    sginfo = parseExtensionSetup('sginfo', config, ext_default)


ext_modules = []
if options['build_levmar']:
    ext_modules.append(Extension('pylevmar', ['src/pylevmar.c'],
                                 extra_compile_args = ['-g'],
                                 depends = ['src/pylevmar.h'],
                                 **levmar))
if options['build_ctrans']:
    ext_modules.append(Extension('ctrans', ['src/ctrans.c'],
                                 depends = ['src/ctrans.h'],
                                 **ctrans))

if options['build_princeton']:
    ext_modules.append(Extension('princeton', ['src/princeton.c'],
                                 depends = ['src/princeton.h'],
				 **princeton))

if options['build_sginfo']:
    ext_modules.append(Extension('pyspec.calcs.sginfo', 
                                 ['src/sginfomodule.c',
                                  'src/sgclib.c',
                                  'src/sgio.c',
                                  'src/sgfind.c',
                                  'src/sghkl.c',
                                  'src/sgsi.c']))
