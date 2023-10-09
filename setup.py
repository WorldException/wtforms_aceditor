#-*-coding:utf8-*-

import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

requires = [
    'wtforms="==2.3.3"',
    'markupsafe',
]

setup(
    name="wtforms_aceditor",
    version="0.1",
    license="GPL",
    description='wtforms aceditor component',
    long_description=read("README.md"),
    author="Stoyanov Evgeny",
    author_email="quick.es@gmail.com",
    url="https://github.com/WorldException/wtforms_aceditor",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
    ],
    packages=['wtforms_aceditor'],
    keywords='wtforms,aceditor,flask',
    requires=requires,
    install_requires=requires,
)