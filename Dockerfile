FROM ubuntu:latest
LABEL authors="chama"

ENTRYPOINT ["top", "-b"]