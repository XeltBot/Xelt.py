#!/usr/bin/env bash

XELTPY_FIRST_START_CHECK = "XELTPY_FIRST_START_CHECK"


if [ ! -f $XELTPY_FIRST_START_CHECK]; then
  touch $XELTPY_FIRST_START_CHECK
  echo 'DO NOT EDIT THIS FILE! THIS IS USED WHEN YOU FIRST RUN XELTPY USING DOCKER' >> $XELTPY_FIRST_START_CHECK
  prisma db push

fi

exec python3 /Xelt/bot/xeltbot.py
