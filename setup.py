# -*- coding: utf8 -*-

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='collective.contact.core',
      version='1.11',
      description="Core package for collective.contact add-ons",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='"Cedric Messiant"',
      author_email='cedricmessiant@ecreall.com',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.contact'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'ExtensionClass',
          'collective.z3cform.datagridfield',
          'collective.contact.widget > 1.2.2',
          'setuptools',
          'ecreall.helpers.upgrade >= 1.1.6.dev0',
          'five.grok',
          'five.globalrequest',
          'plone.api',
          'plone.app.dexterity',
          'plone.app.linkintegrity',
          'plone.app.relationfield',
          'plone.autoform',
          'plone.formwidget.datetime',
          'plone.formwidget.masterselect>=1.3',
          'plone.supermodel',
          'Products.CMFPlone',
          'vobject',
          'zope.schema >= 4.2.1',
      ],
      extras_require={
          'test': ['plone.app.testing',
                   'plone.app.robotframework',
                   'ecreall.helpers.testing',
                   ],
          },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
