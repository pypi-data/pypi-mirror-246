ARG python_version=3.10
FROM python:${python_version}

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /opt

ARG status_page_version=main
RUN git clone --single-branch --branch ${status_page_version} https://github.com/status-page/status-page.git /opt/status-page/ && \
    cd /opt/status-page/ && \
    pip install -r /opt/status-page/requirements.txt && \
    pip install coverage

RUN mkdir -p /plugin
WORKDIR /plugin
COPY . /plugin
COPY development/configuration.py /opt/status-page/statuspage/statuspage/configuration.py
RUN pip install -e .

WORKDIR /opt/status-page/statuspage/
