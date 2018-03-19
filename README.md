# czds-request
Automatically request and renew czdap zones from https://czds.icann.org/

Uses Selenium inside docker to controll a headless web browser and request new zones.

## How to use

Copy `config_sample.py` to `config.py` and set your username, password, and request message.

Run `run.sh` to start the selenium and request containers and request zones.

New zones requested are printed to stdout.


### Automatic requests with cron

To automatically request new zones daily at noon add the following to your crontab:

```
00 12 * * * /path/to/czds-request/run.sh
```

## Building

To build the request image locally instead of pulling from the [docker hub](https://hub.docker.com/r/lanrat/czds-request/) run `build.sh`

