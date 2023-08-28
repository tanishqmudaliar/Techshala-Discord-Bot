import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the bot token from the environment variable
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.tree.command(name="avatar", description="Get user avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.display_avatar)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

# Run the bo
bot.run(token)