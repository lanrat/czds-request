FROM python:2-slim
MAINTAINER Ian Foster <ian@vorsk.com>

# install python-selenium
RUN pip install selenium

ADD request.py /usr/src/czds-request/

WORKDIR /usr/src/czds-request/

CMD ["python", "request.py"]
