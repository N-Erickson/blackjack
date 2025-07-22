FROM python:3.11-alpine

# Only install OpenSSH
RUN apk add --no-cache openssh-server && \
    ssh-keygen -A && \
    mkdir -p /run/sshd && \
    rm -rf /var/cache/apk/*

COPY blackjack.py /root/blackjack.py

RUN echo -e "PermitRootLogin yes\n\
PermitEmptyPasswords yes\n\
PasswordAuthentication yes\n\
ForceCommand /usr/local/bin/python /root/blackjack.py\n\
ClientAliveInterval 30\n\
ClientAliveCountMax 3" >> /etc/ssh/sshd_config && \
    passwd -d root

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
