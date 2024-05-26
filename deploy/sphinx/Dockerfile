FROM alpine:latest

WORKDIR /etc/

RUN mkdir -p /etc/Sphinx/build

RUN apk add --no-cache py3-sphinx py3-sphinx-autobuild

CMD sphinx-autobuild -b html --host 0.0.0.0 --port 8100 /etc/Sphinx/source /etc/Sphinx/build -D language=$LANG