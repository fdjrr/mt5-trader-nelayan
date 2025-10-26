FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbookworm

ENV WINEPREFIX="/config/.wine"

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    python3-pip \
    wget \
    && pip3 install --upgrade pip

RUN wget -q https://dl.winehq.org/wine-builds/winehq.key \
    && apt-key add winehq.key \
    && add-apt-repository 'deb https://dl.winehq.org/wine-builds/debian/ bullseye main' \
    && rm winehq.key

RUN dpkg --add-architecture i386 \
    && apt-get update

RUN apt-get install --install-recommends -y \
    winehq-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY /Metatrader /Metatrader
RUN chmod +x /Metatrader/start.sh
COPY /root /

EXPOSE 3000 8001