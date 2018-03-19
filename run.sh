#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#echo "starting browser"
browser_container=$(docker run --rm --name czds-browser -d selenium/standalone-firefox)
sleep 30

#echo "starting bot"
docker run --rm --name czds-bot --network="container:${browser_container}" -v "${DIR}/config.py:/usr/src/czds-request/config.py:ro" lanrat/czds-request

#echo "stopping browser"
docker stop ${browser_container} >/dev/null

#echo "done"
