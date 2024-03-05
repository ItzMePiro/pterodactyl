import discord
from discord.ext import commands
import subprocess
import random
import string

bot = commands.Bot(command_prefix='!')
authorized_users = ['itzmepiro#0']  # Replace with your Discord username and discriminator
container_info = {}  # Dictionary to store mapping of container IDs to SSH port and password

def generate_password(length=12):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def create_container(ctx):
    if str(ctx.author) not in authorized_users:
        await ctx.send("You are not authorized to use this command.")
        return

    container_id = subprocess.run(["docker", "run", "-d", "-P", "ubuntu"], capture_output=True, text=True).stdout.strip()
    port_mapping = subprocess.run(["docker", "port", container_id], capture_output=True, text=True).stdout.strip()
    container_port = port_mapping.split(':')[-1]
    password = generate_password()
    container_info[container_id] = {'port': container_port, 'password': password}

    # Install and configure openssh-server inside the container
    subprocess.run(["docker", "exec", container_id, "apt", "update"])
    subprocess.run(["docker", "exec", container_id, "apt", "install", "-y", "openssh-server"])
    subprocess.run(["docker", "exec", container_id, "sh", "-c", f"echo 'root:{password}' | chpasswd"])

    # Send SSH info (including random password) to user's DM
    await ctx.author.send(f"Ubuntu container created with SSH access.\nContainer ID: {container_id}\nSSH Port: {container_port}\nRoot Password: {password}")

@bot.command()
async def get_ssh_info(ctx, container_id):
    if str(ctx.author) not in authorized_users:
        await ctx.send("You are not authorized to use this command.")
        return

    if container_id not in container_info:
        await ctx.send("Container ID not found.")
        return

    container_port = container_info[container_id]['port']
    password = container_info[container_id]['password']
    await ctx.send(f"SSH info for container {container_id}:\nSSH Port: {container_port}\nRoot Password: {password}")

bot.run('YOUR_DISCORD_BOT_TOKEN')
