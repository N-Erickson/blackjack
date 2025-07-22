FROM alpine:latest AS builder

# Install Python and OpenSSH
RUN apk add --no-cache python3 openssh-server

# Setup SSH keys
RUN ssh-keygen -A

# Final stage - even slimmer
FROM alpine:latest

# Copy only what we need from builder
COPY --from=builder /etc/ssh/ssh_host_* /etc/ssh/
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /usr/lib/python3* /usr/lib/
COPY --from=builder /usr/sbin/sshd /usr/sbin/sshd

# Install only runtime dependencies (no package manager cache)
RUN apk add --no-cache --no-cache libcrypto3 libssl3 && \
    mkdir -p /run/sshd && \
    rm -rf /var/cache/apk/*

# Copy game
COPY blackjack.py /root/blackjack.py
RUN chmod +x /root/blackjack.py

# Configure SSH for passwordless access
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "ForceCommand /usr/bin/python3 /root/blackjack.py" >> /etc/ssh/sshd_config && \
    echo "ClientAliveInterval 30" >> /etc/ssh/sshd_config && \
    echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config && \
    passwd -d root

# Fly.io expects port 22
EXPOSE 22

# Run SSH daemon
CMD ["/usr/sbin/sshd", "-D", "-e", "-p", "22"]
