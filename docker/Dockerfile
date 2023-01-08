####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10-slim-bullseye AS builder

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt update \
  && apt install -y --no-install-recommends \
  build-essential \
  ca-certificates \
  curl

# Install Poetry locally. This will be needed to produce the wheels
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Xelt

COPY /pyproject.toml /Xelt/
COPY /poetry.lock /Xelt/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev \
  && pip wheel --wheel-dir=/Xelt/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10-slim-bullseye

RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  ca-certificates \
  bash \
  netcat

# Note that wait-for is being copied over. This will be needed for Docker Compose support later
WORKDIR /Xelt
COPY /bot/xeltbot.py /Xelt/bot/
COPY /bot/xeltcore.py /Xelt/bot/
COPY /bot/cogs /Xelt/bot/cogs/
COPY /docker/wait-for /Xelt/wait-for

COPY --from=builder /Xelt/wheels /Xelt/wheels
COPY --from=builder /Xelt/requirements.txt /Xelt/requirements.txt

RUN pip install --upgrade pip setuptools

RUN adduser --disabled-password --gecos "" xelt \
  && chown -R xelt:xelt /Xelt \
  && chmod +x /Xelt/wait-for

USER xelt

ENV PATH="${PATH}:${HOME}/.local/bin"

RUN pip install --user --no-index --find-links=/Xelt/wheels -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

# A start.sh script is needed later for prisma to migrate the models
CMD ["python", "/Xelt/bot/xelt.py"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Xelt.py"
LABEL org.opencontainers.image.description="A high performance multipurpose discord bot with features ranging from user information to music"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/XeltBot/Xelt.py"