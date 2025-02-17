import discord
from discord.ext import commands, tasks
from mcrcon import MCRcon
import re
import random  

# === Configuration (replace these with your own secure settings) ===
TOKEN = "TOKEN_HERE"  # Replace with your actual token or load via environment variable
RCON_HOST = "192.168.1.1"
RCON_PORT = 30116  # Your server's RCON port / RCON port is usually 27016,27016 / IN FSHOST IS  30116
RCON_PASSWORD = "123456" # Your server's RCON Paswword
ALLOWED_ROLE_ID = 123456789  # Your Discord Role ID / Only users with this role may use management commands

# === Intents and Bot Setup ===
intents = discord.Intents.default()
intents.members = True         # Needed for role checks
intents.message_content = True # Needed for text commands

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # Remove default help command to use our custom one

# --- Role Check ---
def has_allowed_role_text(ctx):
    if ctx.guild is None:
        raise commands.CheckFailure("This command can only be used in a server.")
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        return True
    raise commands.CheckFailure("❌ You do not have permission to use this command.")

# --- Error Handler (Send Permission Message Instead of Crashing) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ You do not have permission to use this command.")
    else:
        await ctx.send(f"⚠️ An error occurred: {error}")


# --- Custom Help Command ---
@bot.command(name="help", help="Show help message")
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 CS:GO Server Management Bot Help",
        description="Here is a list of available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(name="📊 !status", value="Show live server status (map & players count)", inline=False)
    embed.add_field(name="👥 !players", value="Show detailed players list", inline=False)
    embed.add_field(name="🗺️ !change_map <map_name>", value="Change the map on the server *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="🎮 !workshop_map <workshop_id>", value="Load a workshop map *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="💬 !say <message>", value="Send a message to in-game chat *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="👢 !kick <player>", value="Kick a player *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="🚫 !ban <player> [duration]", value="Ban a player *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="🔄 !unban <player>", value="Unban a player *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="🕹️ !mode <competitive/wingman> [map_name]", value="Change the game mode *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="❄️ !freezetime <seconds>", value="Set freeze time *(Requires role 'csgo')*", inline=False)
    embed.add_field(name="🗺️ !maps", value="Show available CS:GO maps", inline=False)
    embed.add_field(name="💡 !help", value="Show this help message", inline=False)
    await ctx.send(embed=embed)


# --- Text Command: !status ---
@bot.command(name="status", help="Show live status of the CS:GO server")
async def status(ctx):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command("status")
        map_match = re.search(r'Map\s*"([^"]+)"', response, re.IGNORECASE)
        map_name = map_match.group(1) if map_match else "Unknown"
        players_match = re.search(r"players\s*:\s*(\d+)\s+humans", response, re.IGNORECASE)
        players_count = players_match.group(1) if players_match else "Unknown"
        await ctx.send(f"📊 **Server Status:**\n🗺️ Map: {map_name}\n👥 Players: {players_count}")
    except Exception as e:
        await ctx.send(f"❌ Error retrieving server status: {e}")

# --- Text Command: !players (show detailed players list) ---
@bot.command(name="players", help="Show detailed players list from the server")
async def players(ctx):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command("status")
        players_match = re.search(r"---------players--------\s*\n(.*?)\n#end", response, re.DOTALL)
        if players_match:
            players_list = players_match.group(1).strip()
            await ctx.send(f"👥 **Players List:**\n```{players_list}```")
        else:
            await ctx.send("❌ No players information found.")
    except Exception as e:
        await ctx.send(f"❌ Error retrieving players list: {e}")
        
# --- Text Command: !maps (show CSGO maps list) ---

@bot.command(name="maps", help="Show a list of available CS:GO maps")
async def maps(ctx):
    map_list = [
        "de_dust2", "de_inferno", "de_mirage", "de_nuke", "de_overpass",
        "de_vertigo", "de_ancient", "de_anubis", "de_train", "de_cache"
    ]
    await ctx.send(f"🗺️ **Available Maps:**\n" + "\n".join(map_list))

# --- Text Command: !change_map ---
@bot.command(name="change_map", help="Change the map on the CS:GO server *(Requires role 'csgo')*")
@commands.check(has_allowed_role_text)
async def change_map(ctx, map_name: str):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"changelevel {map_name}")
        await ctx.send(f"🗺️ Map changed to **{map_name}**.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to change map: {e}")

# --- Text Command: !workshop_map ---
@bot.command(name="workshop_map", help="Load a workshop map on the CS:GO server *(Requires role 'csgo')*\nUsage: !workshop_map <workshop_id or URL>")
@commands.check(has_allowed_role_text)
async def workshop_map(ctx, workshop_input: str):
    match = re.search(r"[?&]id=(\d+)", workshop_input)
    workshop_id = match.group(1) if match else workshop_input
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"host_workshop_map {workshop_id}")
        await ctx.send(f"🎮 Workshop map with ID **{workshop_id}** loaded.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to load workshop map: {e}")

# --- Text Command: !say ---
@bot.command(name="say", help="Send a message to in-game chat *(Requires role 'csgo')*")
@commands.check(has_allowed_role_text)
async def say(ctx, *, message: str):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"say {message}")
        await ctx.send(f"💬 Message sent to server: {message}\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to send message: {e}")

# --- Text Command: !mode ---
@bot.command(name="mode", help="Change the game mode on the CS:GO server *(Requires role 'csgo')*\nUsage: !mode <competitive/wingman> [map_name]")
@commands.check(has_allowed_role_text)
async def mode(ctx, mode: str, map_name: str = None):
    try:
        mode = mode.lower()
        if mode == "competitive":
            mode_command = "game_type 0; game_mode 1"
        elif mode == "wingman":
            mode_command = "game_type 0; game_mode 2"
        else:
            return await ctx.send("❌ Invalid mode. Please choose either 'competitive' or 'wingman'.")
        # If no map is provided, try to fetch the current map from the server status.
        if map_name is None:
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                status_response = mcr.command("status")
            map_match = re.search(r'Map\s*"([^"]+)"', status_response, re.IGNORECASE)
            map_name = map_match.group(1) if map_match else "de_inferno"
        command = f"{mode_command}; changelevel {map_name}"
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(command)
        await ctx.send(f"🔄 Game mode changed to **{mode.capitalize()}** on map **{map_name}**.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to change game mode: {e}")

# --- Text Command: !kick ---
@bot.command(name="kick", help="Kick a player from the CS:GO server *(Requires role 'csgo')*")
@commands.check(has_allowed_role_text)
async def kick(ctx, player: str):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"kick {player}")
        await ctx.send(f"👢 Player **{player}** has been kicked.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to kick player: {e}")

# --- Text Command: !ban ---
@bot.command(name="ban", help="Ban a player from the CS:GO server *(Requires role 'csgo')*\nUsage: !ban <player> [duration]")
@commands.check(has_allowed_role_text)
async def ban(ctx, player: str, duration: int = 60):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"banid {duration} {player}")
            mcr.command(f"kick {player}")
        await ctx.send(f"🚫 Player **{player}** has been banned for {duration} minutes.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to ban player: {e}")

# --- Text Command: !unban ---
@bot.command(name="unban", help="Unban a player from the CS:GO server *(Requires role 'csgo')*")
@commands.check(has_allowed_role_text)
async def unban(ctx, player: str):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"removeid {player}")
        await ctx.send(f"✅ Player **{player}** has been unbanned.\nResponse: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to unban player: {e}")
        
# --- Text Command: !freezetime ---
@bot.command(name="freezetime", help="Set the freeze time on the CS:GO server *(Requires role 'csgo')*\nUsage: !freezetime <seconds>")
@commands.check(has_allowed_role_text)
async def freezetime(ctx, seconds: int):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command(f"mp_freezetime {seconds}")
        await ctx.send(f"❄️ Freeze time set to **{seconds}** seconds.\n✅ Response: `{result}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to set freeze time: {e}")

# --- Background Task: Send Welcome Message ---
@tasks.loop(minutes=4)
async def welcome_message():
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            athkar = [
            "سبحان الله",
            "الحمد لله",
            "الله أكبر",
            "لا إله إلا الله",
            "أستغفر الله",
            "اللهم صل وسلم على نبينا محمد",
            "لا حول ولا قوة إلا بالله",
            "سبحان الله وبحمده",
            "سبحان الله العظيم",
            "اللهم أعني على ذكرك وشكرك وحسن عبادتك",
            "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة",
            "اللهم إني أعوذ بك من شر ما عملت ومن شر ما لم أعمل",
            "اللهم جنبني منكرات الأخلاق والأعمال",
            "اللهم اغفر لي ذنبي، إنك أنت الغفور الرحيم",
            "اللهم إني أسألك العفو والعافية"
            ]
            athkar_result = random.choice(athkar)

            mcr.command(f"say {athkar_result}")
            result = mcr.command("say Welcome To Salbeh Server")
        print(f"Sent welcome message: {result}")
    except Exception as e:
        print(f"❌ Failed to send welcome message: {e}")

# --- Background Task: Update Bot Activity with Live Server Status ---
@tasks.loop(seconds=60)
async def update_activity():
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command("status")
        map_match = re.search(r'Map\s*"([^"]+)"', response, re.IGNORECASE)
        map_name = map_match.group(1) if map_match else "Unknown"
        players_match = re.search(r"players\s*:\s*(\d+)\s+humans", response, re.IGNORECASE)
        players_count = players_match.group(1) if players_match else "0"
        
        creative_templates = [
            "🥙 {map_name} - {players_count} falafel fans!",
            "🕌 {map_name} - {players_count} hummus heroes!",
            "🌯 {map_name} - {players_count} shawarma squad!",
            "⚡ {map_name} - {players_count} yalla warriors!"
        ]
        template = random.choice(creative_templates)
        status_text = template.format(map_name=map_name, players_count=players_count)
    except Exception as e:
        status_text = "⚠️ Unable to retrieve server status!"
    
    activity = discord.Game(name=status_text)
    await bot.change_presence(activity=activity)
    print(f"Updated activity to: {status_text}")

# --- On Ready: Start Background Tasks ---
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    welcome_message.start()
    update_activity.start()

# --- Run the Bot ---
bot.run(TOKEN)
