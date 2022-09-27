# We use rockylinux to get as close as we can to RHEL.
# We are using MPI and tend to favor stable API vs new features for EMOD
FROM rockylinux:8
# install all the basic stuff required
RUN dnf install -y dnf-plugins-core epel-release && \
    dnf config-manager --set-enabled powertools
RUN dnf -y update && \
    dnf install -y python39 python39-devel nano which snappy mpich epel-release
# Default to use our productiong package manage. Sometimes we using staging to test new packages when building images
ARG PIP_INDEX_URL=https://packages.idmod.org/api/pypi/pypi-production/simple
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

