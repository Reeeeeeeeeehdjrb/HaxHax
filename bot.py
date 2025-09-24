import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# === CONFIG ===
TOKEN = os.environ.get("DISCORD_TOKEN")
ROLE_NAME = "Approver"  # role required
SHEET_NAME = "Testing Sheet"  # Google Sheet name
ALLOWED_CHANNELS = [
    1243344494993215554,  # replace with your channel IDs
    1245351449240801371,
    333333333333333333,
    444444444444444444,
    555555555555555555,
    666666666666666666,
    777777777777777777,
    888888888888888888,
]

# === DISCORD SETUP ===
intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === GOOGLE SHEETS SETUP ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("empirical-vial-471122-d1-310a360e1df9.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1  # first worksheet

# === EVENTS ===
@bot.event
async def on_ready():
    print(f"{bot.user} is online and logging reactions!")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    # Ignore bot reactions
    if member.bot:
        return

    # Only log in allowed channels
    if payload.channel_id not in ALLOWED_CHANNELS:
        return

    # Check role
    role = discord.utils.get(member.roles, name=ROLE_NAME)
    if not role:
        return

    # Fetch channel + message
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Log message info to Google Sheet
    try:
        sheet.append_row([
            str(message.id),              # message ID
            message.author.display_name,  # who wrote it (nickname)
            message.content,              # message text
            str(payload.emoji),           # emoji used
            member.display_name,          # who reacted (nickname)
        ])
        print(f"Successfully logged to Google Sheet!")
    except Exception as e:
        print(f"Error logging to Google Sheet: {e}")
        print(f"Make sure Google Drive and Sheets APIs are enabled!")

    print(f"Logged from {channel.name}: {message.content} reacted by {member}")

# === RUN BOT ===
bot.run(TOKEN)
