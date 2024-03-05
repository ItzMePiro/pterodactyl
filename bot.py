import discord
from discord.ext import commands
import subprocess
import random
import string

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

authorized_users = ['itzmepiro']  # Replace with your Discord username
container_info = {}  # Dictionary to store mapping of container IDs to SSH ports

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='create-container')
async def create_container(ctx):
    if ctx.author.name not in authorized_users:
        await ctx.send("You are not authorized to use this command.")
        return

    # Generate a random SSH port and password for the container
    ssh_port = random.randint(10000, 65535)
    ssh_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # Run the command to create the container
    # Replace the command below with the actual command to create the container
    create_command = f"create_container_command_here"

    try:
        subprocess.run(create_command.split(), check=True)
        container_info[ctx.author.id] = {'port': ssh_port, 'password': ssh_password}
        await ctx.author.send(f"Container created successfully.\n"
                               f"SSH Port: {ssh_port}\n"
                               f"SSH Password: {ssh_password}")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error creating container: {e}")

# Replace 'your_token_here' with your bot token
bot.run('your_token_here')
