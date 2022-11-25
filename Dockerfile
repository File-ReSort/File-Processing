# syntax=docker/dockerfile:1
FROM python:3.10-slim-bullseye
WORKDIR /File-Processing
RUN pip install coreferee
COPY . .
RUN python setup.py
EXPOSE 3000
CMD [ "flask", "--app" , "main", "run", "--host", "0.0.0.0", "--port", "3000" ]