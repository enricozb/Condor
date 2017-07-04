from setuptools import setup, Extension

condor_module = Extension('condor',
                          sources=['c/condor.c', 'c/glutils.c'],
                          libraries=['GLEW', 'glfw'])

setup (name='Condor',
       version='0.1',
       description='',
       ext_modules=[condor_module])

