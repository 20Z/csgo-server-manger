# 🤖 CS:GO Server Management Bot

Welcome to the **CS:GO Server Management Bot**! 🎮 This bot allows you to control your CS:GO server directly from Discord using **RCON commands**. 🕹️  
## 🧪 Demo
[![Demo](https://i.imgur.com/lFtlzE1.png)](https://salbeh.pw/)

## 🚀 Features
- 📊 **View server status** (`!status`)
- 👥 **List active players** (`!players`)
- 🗺️ **Change maps** (`!change_map <map_name>`)
- 🎮 **Load workshop maps** (`!workshop_map <workshop_id>`)
- 💬 **Send messages to in-game chat** (`!say <message>`)
- 👢 **Kick and ban players** (`!kick <player>` / `!ban <player> [duration]`)
- 🕹️ **Switch game modes** (`!mode <competitive/wingman>`)
- ❄️ **Set freeze time** (`!freezetime <seconds>`)
- 🏆 **Custom Discord bot activity based on server status**
- 🔄 **Automated periodic welcome messages**

## ⚙️ Setup & Installation

```
git clone https://github.com/20Z/csgo-server-manger.git
cd csgo-server-manger
pip install discord.py mcrcon
# Open CSGO_SERVER_MANGER.py and replace:
# - TOKEN with your actual Discord bot token
# - RCON_HOST, RCON_PORT, and RCON_PASSWORD with your CS:GO server’s RCON details
# - ALLOWED_ROLE_ID with the Discord role ID that has bot privileges
# Run the bot
python CSGO_SERVER_MANGER.py
```

## 📜 Commands List
| Command | Description |
|---------|------------|
| `!status` | 📊 Show current server status |
| `!players` | 👥 List active players |
| `!change_map <map_name>` | 🗺️ Change the map (Requires role) |
| `!workshop_map <workshop_id>` | 🎮 Load a workshop map (Requires role) |
| `!say <message>` | 💬 Send a message to in-game chat (Requires role) |
| `!kick <player>` | 👢 Kick a player (Requires role) |
| `!ban <player> [duration]` | 🚫 Ban a player (Requires role) |
| `!unban <player>` | 🔄 Unban a player (Requires role) |
| `!mode <competitive/wingman> [map_name]` | 🕹️ Change the game mode (Requires role) |
| `!freezetime <seconds>` | ❄️ Set freeze time (Requires role) |
| `!maps` | 🗺️ Show available CS:GO maps |
| `!help` | 💡 Show this help message |

## 🔐 Security Notes
- **Never** expose your bot token in public repositories.
- Always **limit bot access** to authorized Discord roles to prevent abuse.
## 🛠️ Troubleshooting
- **Bot not responding?**
  - Check if the bot is online in your Discord server.
  - Verify that the bot has permission to read and send messages in the channel.
  - Ensure `TOKEN`, `RCON_HOST`, and `RCON_PASSWORD` are correct.

- **Commands not working?**
  - Make sure you have the correct **role permissions** (`ALLOWED_ROLE_ID` in the script).
  - Check for typos in commands or required parameters.

## 🏆 Recommended Server Hosting
If you need a high-quality CS:GO server, check out [FSHOST](https://fshost.me/)!
They offer reliable and affordable hosting solutions for CS:GO and other games.
##
Made with ❤️ by [SALBEH](https://salbeh.pw)
