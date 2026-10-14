from setuptools import find_packages
from setuptools import setup

long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)

setup(
    name="collective.contact.core",
    version="2.0.0.dev0",
    description="Core package for collective.contact add-ons",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone contact management organization person position",
    author='"Cedric Messiant"',
    author_email="cedricmessiant@ecreall.com",
    url="https://github.com/collective/collective.contact.core",
    download_url="https://pypi.org/project/collective.contact.core",
    license="gpl",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "collective.contact.widget >= 1.12",
        "collective.js.tooltipster",
        "collective.z3cform.datagridfield",
        "imio.fpaudit",
        "plone.api>=1.4.11",
        "plone.app.dexterity",
        "plone.app.iterate",
        "plone.app.relationfield",
        "plone.app.textfield!=1.2.8",
        "plone.autoform",
        "plone.base",
        "plone.behavior",
        "plone.dexterity",
        "plone.formwidget.masterselect",
        "plone.i18n",
        "plone.indexer",
        "plone.namedfile",
        "plone.schemaeditor",
        "plone.supermodel",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "Products.statusmessages",
        "vobject",
        "z3c.form",
        "z3c.relationfield",
        "zc.relation",
        "Zope",
        "zope.intid",
        "zope.schema >= 4.2.1",
    ],
    extras_require={
        "test": [
            "plone.app.content",
            "plone.app.linkintegrity",
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.testing",
            "robotsuite",
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
