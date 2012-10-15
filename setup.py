from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='collective.z3cinspector',
      version=version,
      description="Zope3 component registry inspector",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope3 component registry inspector',
      author='Jonas Baumann, 4teamwork.ch',
      author_email='mailto:info@4teamwork.ch',
      url='http://github.com/collective/collective.z3cinspector',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        ],
      extras_require={
        'python2.4': [
            'simplejson',
            ],
        },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
