#!/bin/bash
# Complete setup script for CyberJack SSH game on Oracle Cloud
# Run as root or with sudo

echo "🎮 Setting up CyberJack SSH Game Server..."

# 1. Install required packages
echo "📦 Installing packages..."
yum update -y
yum install -y python3 wget git golang openssh-server

# 2. Download the game
echo "🎲 Downloading game..."
mkdir -p /opt/cyberjack
wget https://raw.githubusercontent.com/N-Erickson/blackjack/main/blackjack.py -O /opt/cyberjack/blackjack.py
chmod +x /opt/cyberjack/blackjack.py

# 3. Create cyberjack user (for traditional SSH access)
echo "👤 Creating users..."
useradd -m -s /bin/bash cyberjack 2>/dev/null || true
passwd -d cyberjack

# 4. Move real SSH to port 2022 for admin access
echo "🔧 Configuring SSH..."
sed -i 's/^#*Port.*/Port 2022/' /etc/ssh/sshd_config
systemctl restart sshd

# 5. Disable SELinux (blocks empty passwords)
echo "🔓 Configuring security..."
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config

# 6. Create the Wish proxy
echo "🚀 Building SSH proxy..."
mkdir -p /opt/sshproxy
cd /opt/sshproxy

cat > proxy.go << 'EOF'
package main

import (
    "io"
    "os/exec"
    "github.com/charmbracelet/ssh"
    "github.com/charmbracelet/wish"
    "github.com/creack/pty"
    "log"
)

func main() {
    s, err := wish.NewServer(
        wish.WithAddress(":22"),
        wish.WithHostKeyPath("/etc/ssh/ssh_host_rsa_key"),
        wish.WithPasswordAuth(func(ctx ssh.Context, pass string) bool {
            return true
        }),
        wish.WithPublicKeyAuth(func(ctx ssh.Context, key ssh.PublicKey) bool {
            return true
        }),
        wish.WithMiddleware(func(h ssh.Handler) ssh.Handler {
            return func(s ssh.Session) {
                cmd := exec.Command("/usr/bin/python3", "/opt/cyberjack/blackjack.py")
                
                ptyReq, winCh, isPty := s.Pty()
                if isPty {
                    cmd.Env = append(cmd.Env, "TERM=" + ptyReq.Term)
                    
                    ptmx, err := pty.Start(cmd)
                    if err != nil {
                        log.Printf("Failed to start pty: %v", err)
                        s.Exit(1)
                        return
                    }
                    defer ptmx.Close()
                    
                    go func() {
                        for win := range winCh {
                            pty.Setsize(ptmx, &pty.Winsize{
                                Rows: uint16(win.Height),
                                Cols: uint16(win.Width),
                            })
                        }
                    }()
                    
                    go io.Copy(ptmx, s)
                    io.Copy(s, ptmx)
                    
                    cmd.Wait()
                }
            }
        }),
    )
    
    if err != nil {
        log.Fatal(err)
    }
    
    log.Println("Starting SSH server on :22")
    log.Fatal(s.ListenAndServe())
}
EOF

# Initialize Go module and get dependencies
go mod init sshproxy
go get github.com/charmbracelet/wish
go get github.com/charmbracelet/ssh
go get github.com/creack/pty
go build proxy.go

# 7. Create systemd service
echo "⚙️ Creating service..."
cat > /etc/systemd/system/cyberjack.service << 'EOF'
[Unit]
Description=CyberJack SSH Game Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/sshproxy/proxy
WorkingDirectory=/opt/sshproxy
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 8. Configure firewall
echo "🔥 Configuring firewall..."
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --permanent --add-port=2022/tcp
firewall-cmd --reload

# 9. Start the service
echo "🎯 Starting services..."
systemctl daemon-reload
systemctl enable cyberjack
systemctl start cyberjack

# 10. Show connection info
PUBLIC_IP=$(curl -s ifconfig.me)
echo ""
echo "✅ Setup complete!"
echo ""
echo "🎮 Game Access:"
echo "   ssh $PUBLIC_IP"
echo "   ssh anything@$PUBLIC_IP"
echo "   ssh your-domain.com (after DNS setup)"
echo ""
echo "🔧 Admin Access:"
echo "   ssh -p 2022 opc@$PUBLIC_IP -i your-key.pem"
echo ""
echo "📝 DNS Setup:"
echo "   Add A record: @ → $PUBLIC_IP"
echo ""
echo "🎉 Enjoy CyberJack!"
