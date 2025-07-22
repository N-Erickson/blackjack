FROM alpine:3.18

# Install Python and OpenSSH
RUN apk add --no-cache python3 openssh bash && \
    ssh-keygen -A && \
    mkdir -p /run/sshd

# Copy game
COPY blackjack.py /root/blackjack.py
RUN chmod +x /root/blackjack.py

# Create SSH config without ForceCommand
RUN echo "Port 2222" > /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication no" >> /etc/ssh/sshd_config && \
    echo "StrictModes no" >> /etc/ssh/sshd_config

# Remove root password
RUN passwd -d root

# Set bash as shell
RUN sed -i 's|root:x:0:0:root:/root:/bin/ash|root:x:0:0:root:/root:/bin/bash|' /etc/passwd

# Create .profile to run game on login
RUN echo '#!/bin/bash' > /root/.profile && \
    echo 'exec python3 /root/blackjack.py' >> /root/.profile

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D"]
