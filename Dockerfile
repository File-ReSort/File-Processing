# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
WORKDIR /File-Processing
COPY . .
RUN python setup.py
EXPOSE 50100
CMD [ "python", "main.py" ]