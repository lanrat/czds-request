#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DATE=$(date +%F\ %T)
echo "Running at: $DATE" >> $DIR/request.log

#echo "starting browser"
#browser_container=$(docker run --rm --name czds-browser -d selenium/standalone-firefox)
browser_container=$(docker run --rm --name czds-browser -d selenium/standalone-chrome)
sleep 20

#echo "starting bot"
docker run --rm --name czds-bot --network="container:$browser_container" -v "$DIR/config.py:/usr/src/czds-request/config.py:ro" -v "$DIR/tmp:/tmp" lanrat/czds-request >> $DIR/request.log

#echo "stopping browser"
docker stop ${browser_container} >/dev/null

#echo "done"
