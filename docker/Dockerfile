# csvForWKT - csvForWKT is a python script that creates a WKT-crs for some bodies from the solar system. The content that is filled in the WKT-crs comes from the report of IAU Working Group on Cartographic.
# Copyright (C) 2022 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of csvForWKT.
#
# csvForWKT is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v3  as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# csvForWKT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License v3  for more details.
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with csvForWKT.  If not, see <https://www.gnu.org/licenses/>.
FROM ubuntu:latest

LABEL maintainer="Jean-Christophe Malapert <jean-christophe.malapert@cnes.fr>"

ARG BUILD_DATE
ARG VERSION
ARG DEBIAN_FRONTEND=noninteractive

# Labels (based on http://label-schema.org/rc1/)
LABEL \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="cdm" \
    org.label-schema.description="csvForWKT is a python script that creates a WKT-crs for some bodies from the solar system. The content that is filled in the WKT-crs comes from the report of IAU Working Group on Cartographic." \
    org.label-schema.url="https://github.com/pole-surfaces-planetaires/csvforwkt" \
    org.label-schema.vcs-url="https://github.com/pole-surfaces-planetaires/csvforwkt" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vendor="Pôle Surfaces Planétaires" \
    org.label-schema.version=$VERSION

RUN apt-get update && \
    apt-get install -y \
    software-properties-common apt-transport-https wget git\
    make python3-pip && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    pip install setuptools && \
    git clone "https://github.com/pole-surfaces-planetaires/csvforwkt.git" && \
    cd csvforwkt && \
    make

# Custom prompt
RUN echo 'export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u@platoscope-dev\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$"' >> /etc/bash.bashrc

CMD ["csvforwkt"]
