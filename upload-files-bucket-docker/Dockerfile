# syntax=docker/dockerfile:1

FROM python:3.8

RUN pip3 install requests
RUN pip3 install --upgrade google-cloud-storage

# working directory
WORKDIR /app

# Copy all files from local to docker
COPY . .

CMD ["python3", "main.py"]

#CMD tail -f /dev/null