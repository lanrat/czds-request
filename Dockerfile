FROM python:2-slim
MAINTAINER Ian Foster <ian@vorsk.com>

RUN pip install selenium

ADD request.py /usr/src/czds-request/

USER 1000

WORKDIR /tmp/

CMD ["python", "/usr/src/czds-request/request.py"]
