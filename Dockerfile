FROM python:3.11-alpine

RUN apk add --no-cache openssh-server bash && \
    mkdir -p /run/sshd && \
    ssh-keygen -A

COPY blackjack.py /root/blackjack.py
RUN chmod +x /root/blackjack.py

# Simple config without ForceCommand first
RUN echo "Port 2222" > /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN passwd -d root

# Create a .bashrc that runs the game
RUN echo '#!/bin/bash' > /root/.bashrc && \
    echo 'python3 /root/blackjack.py' >> /root/.bashrc && \
    echo 'exit' >> /root/.bashrc

EXPOSE 2222
CMD ["/usr/sbin/sshd", "-D", "-e", "-p", "2222"]
