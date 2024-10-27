# Author: OnieMikel
# Copyright (c) 2024 Yuto Horiuchi
# License: BSD 3 clause

from setuptools import setup
from yaml import safe_load

with open('config.yml', 'r', encoding='utf-8') as file:
    config_data = safe_load(file)

DESCRIPTION = config_data.get('description')
NAME = config_data.get('name')
AUTHOR = config_data.get('author')
AUTHOR_EMAIL = config_data.get('author_email')
URL = config_data.get('url')
LICENSE = config_data.get('license')
DOWNLOAD_URL = config_data.get('download_url')
VERSION = config_data.get('version')
PYTHON_REQUIRES = config_data.get('python_requires')
UPDATED_DATE = config_data.get('updated_date')

INSTALL_REQUIRES = [
    
]

EXTRAS_REQUIRE = {
    
}

PACKAGES = [
    'ColorPrinter',
]

CLASSIFIERS = [
    
]

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
    print(f"README content: {readme}")  # デバッグ出力

with open('CONTACT.txt', 'r', encoding='utf-8') as fp:
    contacts = fp.read()
    print(f"CONTACT content: {contacts}")  # デバッグ出力
long_description = readme + '\n\n' + contacts

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
      release_date=UPDATED_DATE
    )
