FROM alpine:3.4
MAINTAINER toolbox@cloudpassage.com

ENV HALO_SCANS_GIT=https://github.com/cloudpassage/halo-scans
ENV HALO_SCANS_VERSION=v0.9

ENV HALO_API_HOSTNAME=api.cloudpassage.com
ENV HALO_API_PORT=443

ENV DROP_DIRECTORY=/var/scans

RUN apk add --no-cache \
    git=2.8.3-r0 \
    python=2.7.12-r0 \
    py-pip=8.1.2-r0

RUN mkdir /app
COPY ./ /app/

RUN mkdir /src/
WORKDIR /src/
RUN git clone ${HALO_SCANS_GIT}
WORKDIR /src/halo-scans
RUN git checkout ${HALO_SCANS_VERSION}
RUN pip install .

WORKDIR /app/tool/

RUN pip install \
    boto3==1.4.2 \
    codeclimate-test-reporter==0.2.0 \
    coverage==4.2 \
    pytest==2.8.0 \
    pytest-cover==3.0.0 \
    pytest-flake8==0.1

RUN py.test --cov=scanslib

RUN mkdir -p $DROP_DIRECTORY

CMD python /app/tool/runner.py
