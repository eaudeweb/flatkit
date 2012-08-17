import os.path
import distutils.core


summary = ("flatkit is a library of utilities for projects that are based on "
           "Flask, Flatland and Htables.")


distutils.core.setup(
    name='flatkit',
    url='http://github.com/eaudeweb/flatkit/',
    description=summary,
    version='dev',
    author='Eau de Web',
    author_email='office@eaudeweb.ro',
    py_modules=['flatkit'],
)
