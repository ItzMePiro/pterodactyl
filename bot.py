import discord
from discord.ext import commands
import paramiko
import random
import string

# Configuration
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
VPS_IPv6 = 'YOUR_VPS_IPV6_ADDRESS'  # Replace with your VPS IPv6 address
SSH_USERNAME = 'YOUR_SSH_USERNAME'
PRIVATE_KEY_PATH = '/root/.ssh/id_rsa'

# Bot setup with intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Define a subclass of Bot to properly pass the intents parameter
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

bot = MyBot()

# Function to create a container with custom SSH port
def create_container():
    container_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    ssh_port = random.randint(49152, 65535)  # Randomly select a port in the dynamic/private port range
    ssh_command = f'docker run -d -p {ssh_port}:22 --name {container_id} ubuntu'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=VPS_IPv6, username=SSH_USERNAME, key_filename=PRIVATE_KEY_PATH)
    stdin, stdout, stderr = ssh_client.exec_command(ssh_command)
    ssh_client.close()
    return container_id, ssh_port

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Bot commands
@bot.command(name="create-container")
async def create_container_command(ctx):
    container_id, ssh_port = create_container()
    await ctx.send(f"Container created with ID: {container_id}, SSH port: {ssh_port}")

# Run the bot
bot.run(TOKEN)
