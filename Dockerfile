FROM python:3.11-alpine

# Install OpenSSH and bash for debugging
RUN apk add --no-cache openssh-server bash && \
    mkdir -p /run/sshd /root/.ssh

# Generate SSH host keys
RUN ssh-keygen -A

# Copy game
COPY blackjack.py /root/blackjack.py
RUN chmod +x /root/blackjack.py

# Create a simple SSH config
RUN echo "Port 2222" > /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication no" >> /etc/ssh/sshd_config && \
    echo "UsePAM no" >> /etc/ssh/sshd_config

# Remove root password
RUN passwd -d root

# Create a startup script that will help us debug
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'echo "Starting SSH daemon..."' >> /start.sh && \
    echo 'echo "Testing SSH config..."' >> /start.sh && \
    echo '/usr/sbin/sshd -t -f /etc/ssh/sshd_config' >> /start.sh && \
    echo 'if [ $? -ne 0 ]; then' >> /start.sh && \
    echo '  echo "SSH config test failed!"' >> /start.sh && \
    echo '  exit 1' >> /start.sh && \
    echo 'fi' >> /start.sh && \
    echo 'echo "Starting sshd on port 2222..."' >> /start.sh && \
    echo 'exec /usr/sbin/sshd -D -e -p 2222' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 2222

# Use the debug script
CMD ["/start.sh"]
