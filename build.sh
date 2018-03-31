#!/usr/bin/env sh

docker pull python:2-slim

docker build -t lanrat/czds-request .

