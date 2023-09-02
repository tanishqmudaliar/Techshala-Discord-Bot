import os
import openai
import discord
from discord import File
from easy_pil import Editor, load_image_async, Font
from discord.ext import commands
from dotenv import load_dotenv
from webserver import keepalive

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Retrieve the bot token from the environment variable
token = os.getenv("BOT_TOKEN")

# Initialize intents
intents = discord.Intents.all()

# Initialize the bot with commands and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Command to interact with GPT-3 and get a response
# @bot.tree.command(name="chat", description="Chat with the bot")
# async def chat(interaction: discord.Interaction, message: str):
#     messages = [
#         {"role": "user", "content": message}
#     ]

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=0.7,
#         max_tokens=150
#     )

#     await interaction.response.send_message(response.choices[0].message["content"])

# Command to get user's avatar
@bot.tree.command(name="avatar", description="Get a user's avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}'s avatar", colour=discord.Colour.green())
    embed.set_image(url=member.avatar.url)
    embed.set_footer(text=f"This is the avatar from {member.name} #{member.discriminator}", icon_url=bot.user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="Kick a member from the server")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.guild_permissions.kick_members:  # Check if the command issuer has required permissions
        await member.send(f">>> You have been kicked from {interaction.guild.name} by {interaction.user.mention} for the following reason: '{reason}'")
        await interaction.response.send_message(f">>> {member.mention} has been kicked by {interaction.user.mention} for the following reason: '{reason}'")
        await member.kick(reason=reason)
    else:
        await interaction.response.send_message(">>> You don't have the necessary permissions to use this command.")

@bot.tree.command(name="ban", description="Ban a member from the server")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.guild_permissions.ban_members:  # Check if the command issuer has required permissions
        await member.send(f">>> You have been banned from {interaction.guild.name} by {interaction.user.mention} for the following reason: '{reason}'")
        await interaction.response.send_message(f">>> {member.mention} has been banned by {interaction.user.mention} for the following reason: '{reason}'")
        await member.ban(reason=reason)
    else:
        await interaction.response.send_message(">>> You don't have the necessary permissions to use this command.")

# Event when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Destroying thw world"))
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_member_join(member):
    channel_id = 1146390103162355732 # Replace with the actual channel ID
    channel = member.guild.get_channel(channel_id)
    background = Editor("banner.png")
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((400, 400)).circle_image()
    font_style = Font.poppins(size=40, variant="bold")
    font_style_small = Font.poppins(size=25, variant="light")
    background.paste(profile, (125,300))
    background.ellipse((125,300),400,400, outline="green", stroke_width=5)
    background.text((328, 730),  f"Welcome to {member.guild.name}", color="black", font=font_style, align="center")
    background.text((328, 780),  f"{member.name} #{member.discriminator}", color="black", font=font_style_small, align="center")
    file = File(fp=background.image_bytes, filename="banner.png")
    await channel.send(file=file)

# Run the bot
keepalive()
bot.run(token)