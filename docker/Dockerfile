FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  tini \
  bash \
  netcat-traditional \
  git \
  && apt-get clean

WORKDIR /xelt
COPY /bot /xelt/bot/
COPY /docker/start.sh /xelt/start.sh
COPY /docker/wait-for /xelt/wait-for
COPY /requirements.txt /xelt/requirements.txt

RUN adduser --disabled-password --gecos "" xelt \
  && chown -R xelt:xelt /xelt \
  && chmod +x /xelt/start.sh \
  && chmod +x /xelt/wait-for

USER xelt

ENV PATH="${PATH}:${HOME}/.local/bin"

RUN pip install --user -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/xelt/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Xelt.py"
LABEL org.opencontainers.image.description="A high performance multipurpose discord bot with features ranging from user information to music"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/XeltBot/Xelt.py"
