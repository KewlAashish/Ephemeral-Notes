# 1) Use Python base image
FROM python:3.9-slim

# 2) Install Redis
RUN apt-get update && apt-get install -y redis-server

# 3) Create a working directory
WORKDIR /app

# 4) Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5) Copy your application code
COPY . /app/

# 6) Expose the Flask port
EXPOSE 5000

# 7) Start Redis in the background, then run Flask
CMD redis-server --daemonize yes && python app/main.py
