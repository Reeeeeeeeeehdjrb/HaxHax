import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# === CONFIG ===
TOKEN = os.environ.get("DISCORD_TOKEN")
ROLE_NAME = "Approver"
SHEET_NAME = "Testing Sheet"
ALLOWED_CHANNELS = [
    1243344494993215554,
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

# === GOOGLE SHEETS SETUP FROM ENV VAR ===
# Store your JSON creds as a single environment variable called GOOGLE_CREDS_JSON
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
if not creds_json:
    raise ValueError("GOOGLE_CREDS_JSON environment variable not set!")

creds_dict = json.loads(creds_json)
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# === EVENTS ===
@bot.event
async def on_ready():
    print(f"{bot.user} is online and logging reactions!")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member.bot:
        return
    if payload.channel_id not in ALLOWED_CHANNELS:
        return
    role = discord.utils.get(member.roles, name=ROLE_NAME)
    if not role:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    try:
        sheet.append_row([
            str(message.id),
            message.author.display_name,
            message.content,
            str(payload.emoji),
            member.display_name,
        ])
        print("Successfully logged to Google Sheet!")
    except Exception as e:
        print(f"Error logging to Google Sheet: {e}")

    print(f"Logged from {channel.name}: {message.content} reacted by {member}")

# === RUN BOT ===
bot.run(TOKEN)
