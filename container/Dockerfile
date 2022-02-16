FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

# Mandatory soft
RUN apt update -y && apt install -y iptables redsocks tzdata

# Optional soft
RUN apt update -y && apt install -y mc htop git curl gpg-agent

# Adjust; TODO: make configurable, hardcoding is shit
ENV TZ=Europe/Moscow

COPY entry.sh /entry.sh
ENTRYPOINT ["/entry.sh"]
