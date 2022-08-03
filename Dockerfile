FROM python:3.7

RUN pip install --upgrade pip && \
    pip install bs4 requests python-magic pyyaml
