from setuptools import setup

try:
    # python2
    execfile('okp/version.py')
except NameError as e:
    # python3
    eval('exec(open("./okp/version.py").read())')

setup(
    name='okp',
    version=__version__,
    author='okay',
    author_email='okayzed+okp@gmail.com',
    include_package_data=True,
    packages=['okp', 'okp.transforms'],
    scripts=['scripts/okp'],
    url='http://github.com/okayzed/okp',
    license='MIT',
    description='an compiler for .cpy files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[ "future" ],
    )

