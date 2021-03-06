FROM ubuntu:18.04



WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    python3.4 \
    python \
    python3-pip\
    git\
    wget\
    nano
RUN pip3 --no-cache-dir install -r requirements.txt
RUN cd api/tools/ && git clone https://github.com/shmilylty/OneForAll.git
RUN pip3 --no-cache-dir install -r api/tools/Sublist3r/requirements.txt
RUN pip3 --no-cache-dir install -r api/tools/OneForAll/requirements.txt

RUN sh -c "echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list.d/kali.list"
RUN apt install -y gnupg
RUN wget 'https://archive.kali.org/archive-key.asc'
RUN apt-key add archive-key.asc
RUN sh -c "echo 'Package: *'>/etc/apt/preferences.d/kali.pref; echo 'Pin: release a=kali-rolling'>>/etc/apt/preferences.d/kali.pref; echo 'Pin-Priority: 50'>>/etc/apt/preferences.d/kali.pref"
RUN apt update

RUN apt -y  install eyewitness
RUN apt -y install amass

RUN apt-get install -y redis-server
RUN pip3 --no-cache-dir install  celery
RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

RUN cp api/tools/nabbu/naabu-linux-amd64 /usr/local/bin/naabu

RUN cp api/tools/nuclei/nuclei /usr/local/bin/

RUN tar -C /usr/local -xzf api/tools/go/go1.6.linux-amd64.tar.gz
RUN export PATH=$PATH:/usr/local/go/bin

RUN mkdir certs
RUN cd certs && openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=na/ST=na/L=nad/O=na/CN=na.com"
RUN cd static && mkdir output

EXPOSE 5000
