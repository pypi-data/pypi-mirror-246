"""Setup script for godel package.
"""
import glob

DISTNAME = 'godel-jupyter'
DESCRIPTION = 'A Jupyter kernel for Godel.'
LONG_DESCRIPTION = open('README.md', 'rb').read().decode('utf-8')
MAINTAINER = 'ZHENG Xunjin'
MAINTAINER_EMAIL = 'zhengxunjin.zx@antgroup.com'
REQUIRES = [
    "metakernel (>=0.30.1)",
    "jupyter_client (>=4.3.0)",
    "ipykernel",
    "pandas",
]
INSTALL_REQUIRES = [
    "metakernel >=0.30.1",
    "jupyter_client >=4.3.0",
    "ipykernel",
    "pandas",
]
PACKAGES = [DISTNAME]
PACKAGE_DATA = {
    DISTNAME: ['*.m'] + glob.glob('%s/**/*.*' % DISTNAME)
}
DATA_FILES = [
    ('share/jupyter/kernels/godel-jupyter', [
        '%s/kernel.json' % DISTNAME
    ] + glob.glob('%s/images/*.png' % DISTNAME)
     )
]

from setuptools import setup

with open('godel-jupyter/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(
    name=DISTNAME,
    version=version,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    data_files=DATA_FILES,
    platforms=["Any"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    requires=REQUIRES,
    install_requires=INSTALL_REQUIRES
)
