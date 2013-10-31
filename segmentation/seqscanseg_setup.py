from distutils.core import setup, Extension

import numpy

seqscanseg_module = Extension('seqscanseg',
								sources = ['seqscanseg.c', 'seqscanseg_impl.cpp'],
								include_dirs = [numpy.get_include()])

setup (name = 'seqscanseg',
		version = '1.0',
		description = 'Sequence scanline segmentation',
		ext_modules = [seqscanseg_module])
