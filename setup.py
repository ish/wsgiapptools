from setuptools import setup, find_packages
import sys, os

version = '0.5'

setup(name='wsgiapptools',
      version=version,
      description="Collection of WSGI application tools",
      long_description="""\
""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Environment :: Web Environment"
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Internet :: WWW/HTTP :: WSGI",
          "Topic :: Software Development :: Libraries :: Python Modules"
          "Topic :: Software Development :: Widget Sets",
          "Topic :: Internet",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Browsers", 
      ], 
      keywords='wsgi,messages,cookie',
      author='Tim Parkin, Matt Goodall',
      author_email='developers@ish.io',
      url='http://ish.io/projects/show/wsgiapptools',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
