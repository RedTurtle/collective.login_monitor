from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='collective.login_monitor',
      version=version,
      description="Store and monitor login access to your Plone site",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov login user access monitor',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.saconfig',
          'SQLAlchemy',
          'collective.js.jqueryui',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
