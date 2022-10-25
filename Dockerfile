FROM python:3.10-slim

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/src/

RUN apt-get update && apt-get install -y \
  build-essential \
  && apt-get clean

COPY ./requirements.txt ./setup.cfg ./black.toml ./.pylintrc /

RUN pip install --upgrade pip -r /requirements.txt

ADD ./src /src
ADD ./docs /docs
WORKDIR /src

# root is used as a hotfix for package introspection problem
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000373944/comments/7286554132370
USER root
