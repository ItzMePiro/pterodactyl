import discord
from discord.ext import commands
import paramiko
import random
import string

# Configuration
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
VPS_IP = 'YOUR_VPS_IP'
SSH_USERNAME = 'YOUR_SSH_USERNAME'
PRIVATE_KEY_PATH = 'PATH_TO_YOUR_PRIVATE_KEY'

# Bot setup
bot = commands.Bot(command_prefix='!')

# Function to create a container
def create_container():
    container_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=VPS_IP, username=SSH_USERNAME, key_filename=PRIVATE_KEY_PATH)
    stdin, stdout, stderr = ssh_client.exec_command(f'docker run -d --name {container_id} ubuntu')
    ssh_client.close()
    return container_id

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Bot commands
@bot.command(name="create-container")
async def create_container_command(ctx):
    container_id = create_container()
    await ctx.send(f"Container created with ID: {container_id}")

# Run the bot
bot.run(TOKEN)
