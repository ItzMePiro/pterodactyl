import discord
from discord.ext import commands
import subprocess
import random

bot = commands.Bot(command_prefix='!')
authorized_users = ['itzmepiro#0000']  # Update with your Discord username and discriminator
container_ports = {}  # Dictionary to store mapping of container IDs to SSH ports

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
    container_ports[container_id] = container_port

    await ctx.send(f"Ubuntu container created with SSH access. SSH port: {container_port}")

@bot.command()
async def get_ssh_port(ctx, container_id):
    if str(ctx.author) not in authorized_users:
        await ctx.send("You are not authorized to use this command.")
        return

    if container_id not in container_ports:
        await ctx.send("Container ID not found.")
        return

    container_port = container_ports[container_id]
    await ctx.send(f"SSH port for container {container_id}: {container_port}")

bot.run('YOUR_DISCORD_BOT_TOKEN')
