from setuptools import find_packages
from setuptools import setup

import os


def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()


version = "2.0.0"

setup(
    name="collective.portletmetadata",
    version=version,
    description="Adds metadata functionality to portlets",
    long_description="\n".join(
        [
            read("README.rst"),
            read("CHANGES.rst"),
        ]
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="portlets metadata class",
    author="Bo Simonsen",
    author_email="bo@headnet.dk",
    url="http://github.com/collective/collective.portletmetadata",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "collective.monkeypatcher",
        "plone.app.portlets",
        "plone.app.registry",
        "plone.autoform",
        "plone.base",
        "plone.memoize",
        "plone.portlets",
        "Products.GenericSetup",
        "setuptools",
        "z3c.form",
        "z3c.jbot",
        "z3c.unconfigure>=1.0.1",
    ],
    extras_require={
        "test": [
            "plone.testing",
            "plone.app.testing",
        ],
    },
    entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
    """,
)
