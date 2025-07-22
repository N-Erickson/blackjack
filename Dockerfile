FROM alpine:3.18

RUN apk add --no-cache python3 openssh bash && \
    ssh-keygen -A && \
    mkdir -p /run/sshd

COPY blackjack.py /root/blackjack.py
RUN chmod +x /root/blackjack.py

# SSH config for port 22 (standard SSH port with dedicated IP)
RUN echo "Port 22" > /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication no" >> /etc/ssh/sshd_config && \
    echo "StrictModes no" >> /etc/ssh/sshd_config

RUN passwd -d root && \
    sed -i 's|root:x:0:0:root:/root:/bin/ash|root:x:0:0:root:/root:/bin/bash|' /etc/passwd

# Auto-run game on login
RUN echo '#!/bin/bash' > /root/.profile && \
    echo 'exec python3 /root/blackjack.py' >> /root/.profile

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
