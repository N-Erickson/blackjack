FROM alpine:3.18

# Install Python and OpenSSH
RUN apk add --no-cache python3 openssh-server bash && \
    ssh-keygen -A && \
    mkdir -p /run/sshd

# Copy the game
COPY blackjack.py /root/blackjack.py
RUN chmod 755 /root/blackjack.py

# Create proper SSH configuration
RUN cat > /etc/ssh/sshd_config <<EOF
Port 2222
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
PermitRootLogin yes
PermitEmptyPasswords yes
PasswordAuthentication yes
ChallengeResponseAuthentication no
PubkeyAuthentication no
PrintMotd no
PrintLastLog no
Subsystem sftp /usr/lib/ssh/sftp-server
ForceCommand /usr/bin/python3 /root/blackjack.py
EOF

# Set root shell and remove password
RUN sed -i 's|root:x:0:0:root:/root:/bin/ash|root:x:0:0:root:/root:/bin/bash|' /etc/passwd && \
    passwd -d root

# Test configuration
RUN /usr/sbin/sshd -t

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D", "-e"]
