#
# Copyright (c) 2007 Vee Satayamas
# 
# This file is part of WordBreak TST.
# 
# KunyitTst is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# KunyitTst is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
import os
setup(name="wordbreaktst",
      version="0.0.2",
      description="A pure Python ternary search tree library",
      long_description="""
A pure Python ternary search tree library
""",
      author="Vee Satayamas",
      author_email="vsatayamas@gmail.com",
      license = "LGPL",
      packages=['wordbreaktst'],
      scripts=[os.path.join("scripts", "buildtst")],
      test_suite="nose.collector",
      url = "https://bitbucket.org/veer66/wordbreaktst",
      #download_url = "http://code.google.com/p/kunyittst/downloads/list",
      classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Text Processing',
        'Topic :: Scientific/Engineering :: Information Analysis'
      ])
