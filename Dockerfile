FROM python:3.9-slim AS base

# python:
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app
# pip:
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100
# poetry:
ENV POETRY_VERSION 1.3.2
ENV POETRY_VIRTUALENVS_CREATE false
ENV POETRY_CACHE_DIR '/var/cache/pypoetry'

# Install system dependencies
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  build-essential \
  gettext \
  libpq-dev \
  wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && pip install "poetry-core==1.4.0" "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/

# Project initialization:
RUN poetry install

# Creating folders, and files for a project:
COPY . /code

CMD ["bash"]
