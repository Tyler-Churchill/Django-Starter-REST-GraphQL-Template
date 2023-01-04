FROM python:3.11.1

# TODO change to multi-stage docker image (base, dev, prod)

# Keeps Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Effecient container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y postgresql

# Install Poetry
COPY ./scripts .
ENV POETRY_HOME=/poetry
RUN python get-poetry.py --version 1.2.0
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

# Install Deps
# Install any dependencies, this step will be cached so long as pyproject.toml is unchanged
ADD poetry.lock pyproject.toml /app/code/
WORKDIR /app/code
RUN poetry install

# Install the project itself (this is almost never cached)
COPY . /app/code

# Add custom commands (not django manage.py commands, but custom CLI QoL)
RUN chmod +x commands/*
ENV PATH="commands:${PATH}"

EXPOSE 8000
CMD ["poetry shell"]