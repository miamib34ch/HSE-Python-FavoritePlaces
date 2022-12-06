# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/src/ \
  # Disable pip cache to make docker image smaller
  PIP_NO_CACHE_DIR=1 \
  # Disable pip version check
  PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    build-essential \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./setup.cfg ./black.toml ./.pylintrc /

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip -r /requirements.txt

ADD ./src /src
ADD ./docs /docs
WORKDIR /src

# root is used as a hotfix for package introspection problem
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000373944/comments/7286554132370
USER root
