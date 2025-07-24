# 🎰 CyberJack SSH Casino

> A blackjack game accessible directly through SSH.

```
 ▄████▄ ▓██   ██▓ ▄▄▄▄  ▓█████ ██▀███        ░▄▄▄▄▄ ▄▄▄▄▄░  ▄████▄ ██ ▄█▀
▒██▀ ▀█  ▒██  ██▒▓████▄ ▓█   ▀▓██ ▒ ██▒      ░░██▀ ▒█▄▄▄█░ ▒██▀ ▀█ ██▄█▒ 
▒▓█    ▄  ▒██ ██░▒██▒▄██▒███  ▓██ ░▄█ ▒      ░▄█  ░█▄▄▄█░ ▒▓█    ▄ ██▄█▒ 
▒▓▓▄ ▄██▒ ░ ▐██▓░▒██░█▀ ▒▓█  ▄▒██▀▀█▄        ░▄█▄▄█▀   ░▀ ▒▓▓▄ ▄██▒▓███▄ 
▒ ▓███▀ ░ ░ ██▒▓░░▓█ ▀█▓░▒████░██▓ ▒██▒       ░▀▀▀    ░   ▒ ▓███▀ ░▓██ █▄
```

## 🎲 Play Now

```bash
ssh cyberdeck.casino
```

That's it.

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │   SSH   │                  │  Exec   │                 │
│  Your Terminal  ├────────►│   Wish Proxy     ├────────►│  Blackjack.py   │
│                 │  :22    │  (Port 22)       │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     │ Admin SSH
                                     │ :2022
                                     ▼
                            ┌──────────────────┐
                            │   Admin Access   │
                            │  (Port 2022)     │
                            └──────────────────┘
```

## 🚀 Deployment

### Prerequisites
- Oracle Cloud Free Tier instance (or any VPS)
- Domain name
- 15 minutes

### Quick Deploy

1. **Launch Oracle Cloud instance** with Oracle Linux

2. **Run the setup script**:
```bash
curl -sSL https://raw.githubusercontent.com/N-Erickson/blackjack/main/ocisetup.sh | sudo bash
```

3. **Point your domain** to the server IP:
   - Add A record: `@ → your-server-ip`

4. **Play**:
```bash
ssh cyberdeck.casino
```

## 🛠️ Technical Stack

- **Game Engine**: Python 3
- **SSH Server**: [Wish](https://github.com/charmbracelet/wish) (Go)
- **Terminal UI**: ANSI escape codes
- **Hosting**: Oracle Cloud Free Tier
- **Authentication**: None required!

## 📊 How It Works

```
User Flow:
═════════

ssh cyberdeck.casino
    │
    ▼
┌─────────────────────────┐
│   DNS Resolution        │
│ cyberdeck.casino → IP   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Wish SSH Server       │
│   Listening on :22      │
│   • Accepts any user    │
│   • No password needed  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Python Subprocess     │
│   blackjack.py          │
│   • Full terminal I/O   │
│   • ANSI color support  │
└───────────┬─────────────┘
            │
            ▼
        🎰 PLAY! 🎰
```

## 🎮 Game Features

### Betting System
- Starting balance: $500
- Minimum bet: $5
- All bets in $5 increments

### Blackjack Rules
- Dealer hits soft 17
- Blackjack pays 3:2
- Double after split allowed
- Split any pair (including 10-value cards)
- No insurance or surrender

### Terminal Features
- Full color support with cyberpunk theme
- ASCII card art
- Responsive to terminal size

## 🌐 Browser Fallback

For users without native SSH clients:

### Windows
```powershell
# Built-in OpenSSH (Windows 10+)
ssh cyberdeck.casino

# Or use PuTTY
```

<img width="737" height="795" alt="image" src="https://github.com/user-attachments/assets/1296d330-7638-4474-88c8-66e3a344f1a8" />



## 🎯 Roadmap

- [ ] Multiplayer tables
- [ ] Poker variant
- [ ] Slot machines
- [ ] High score tracking
- [ ] Tournament mode
- [ ] Web-based terminal
- [ ] More casino games
