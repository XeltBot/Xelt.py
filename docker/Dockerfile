####################################################################################################
## Builder image
####################################################################################################
FROM python:3.11-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive 

# We will need git later...
RUN apt update \
  && apt install -y --no-install-recommends \
  build-essential \
  ca-certificates \
  curl \
  git

# Install Poetry locally. This will be needed to produce the wheels
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Xelt

COPY /pyproject.toml /Xelt/
COPY /poetry.lock /Xelt/

# Save the dependencies as wheels (.whl)
# In order to get this ready for production, the dev dependencies are not included
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main \
  && pip wheel --wheel-dir=/Xelt/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.11-slim-bookworm

# The last two are required libraries for proper voice support on discord.py (Note that python3-dev is not included)
# Python's C headers are included when the Python interpreter is being compiled
RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  ca-certificates \
  bash \
  netcat-traditional \
  libnacl-dev \
  libopus-dev \
  libffi-dev \
  git

# Note that wait-for is being copied over. This will be needed for Docker Compose support later
WORKDIR /Xelt
COPY /bot/xeltbot.py /Xelt/bot/
COPY /bot/xeltcore.py /Xelt/bot/
COPY /bot/cogs /Xelt/bot/cogs/
COPY /docker/wait-for /Xelt/wait-for
COPY /docker/start.sh /Xelt/start.sh
COPY /migrate.py /Xelt/migrate.py
COPY /migrations /Xelt/migrations/

# Copy over all of the wheels and requirements.txt
COPY --from=builder /Xelt/wheels /Xelt/wheels
COPY --from=builder /Xelt/requirements.txt /Xelt/requirements.txt

# Always a good idea to upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# We want to run everything now as a non-root user
# By default, inside a Docekr container, all of the files and scripts are ran as root
# This is insecure by default
RUN adduser --disabled-password --gecos "" xelt \
  && chown -R xelt:xelt /Xelt \
  && chmod +x /Xelt/wait-for \
  && chmod +x /Xelt/start.sh

USER xelt

# Mainly to get the executables working
ENV PATH="${PATH}:/home/xelt/.local/bin"

# Finalally actually install all of the libraries
RUN pip install --user --no-index --find-links=/Xelt/wheels -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["Xelt/start.sh"]

STOPSIGNAL SIGTERM

# Metadata
LABEL org.opencontainers.image.title="Xelt.py"
LABEL org.opencontainers.image.description="A high performance multipurpose discord bot with features ranging from user information to music"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/XeltBot/Xelt.py"
