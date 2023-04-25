FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip3 install -r requirements.txt

COPY . .
# Add this:
ENV FLASK_APP=app.py
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
