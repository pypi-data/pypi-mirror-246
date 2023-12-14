#!/bin/bash
#
# Build manylinux wheels for HTSeq. Based on the example at
# <https://github.com/pypa/python-manylinux-demo>
#
# It is best to run this in a fresh clone of the repository!
#
# Run this within the repository root:
#   docker run --rm -v $(pwd):/io quay.io/pypa/manylinux2010_x86_64 /io/buildwheels.sh
#
# The wheels will be put into the wheelhouse/ subdirectory.
#
# For interactive tests:
#   docker run -it -v $(pwd):/io quay.io/pypa/manylinux2010_x86_64 /bin/bash

set -xeuo pipefail

echo "Install zlib dev libraries for HTSlib when needed"
# manylinux2010 is CentOS 6, manylinux2014 is CentOS 7
yum -y install zlib-devel bzip2-devel xz-devel wget

echo "Install SWIG (CentOS 6 has an old one!)"
#wget http://springdale.princeton.edu/data/springdale/6/x86_64/os/Computational/swig3012-3.0.12-3.sdl6.x86_64.rpm
#rpm -Uvh swig3012-3.0.12-3.sdl6.x86_64.rpm
wget http://springdale.princeton.edu/data/springdale/7/x86_64/os/Computational/swig3012-3.0.12-3.sdl7.x86_64.rpm
rpm -Uvh swig3012-3.0.12-3.sdl7.x86_64.rpm
yum -y install swig3012

echo "Remove old Python versions"
rm -rf /opt/python/cp27*
rm -rf /opt/python/cpython-2.7*
rm -rf /opt/python/cp33*
rm -rf /opt/python/cp34*
rm -rf /opt/python/cp35*
rm -rf /opt/python/cp36*
