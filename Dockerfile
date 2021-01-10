FROM ubuntu:18.04



WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    python3.4 \
    python3-pip
RUN pip3 --no-cache-dir install -r requirements.txt


EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]
