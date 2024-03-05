import discord
from discord.ext import commands
import subprocess
import random
import string

intents = discord.Intents.default()
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

authorized_users = ['itzmepiro']  # Replace with authorized Discord usernames
container_info = {}  # Dictionary to store container information

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Register the slash command
    await bot.application.commands.extend([
        discord.ApplicationCommand(
            name="vm-create",
            description="Create a virtual machine container",
            options=[
                discord.Option(
                    type=3,
                    name="name",
                    description="Name for the container",
                    required=True
                )
            ]
        )
    ])

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.slash_command(name="vm-create")
async def create_container(ctx, name: str):
    if str(ctx.author) not in authorized_users:
        await ctx.send("You are not authorized to use this command.")
        return
    
    container_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    ssh_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    ssh_port = random.randint(10000, 60000)  # Generate a random port between 10000 and 60000
    
    # Run Docker command to create container
    subprocess.run(f"docker run -d -p {ssh_port}:22 --memory=1g --cpus=0.5 --name {container_id} ubuntu", shell=True)
    
    # Set SSH password
    subprocess.run(f"docker exec {container_id} bash -c 'echo \"root:{ssh_password}\" | chpasswd'", shell=True)
    
    # Store container information
    container_info[container_id] = {'ssh_password': ssh_password, 'ssh_port': ssh_port}
    
    # Send container information to user's DM
    user = ctx.author
    dm_channel = await user.create_dm()
    await dm_channel.send(f"Container {name} created. SSH port: {ssh_port}, SSH password: {ssh_password}")
    await dm_channel.send("To SSH into the VPS, use the following command:\n"
                          f"`ssh root@YOUR_SERVER_IP -p {ssh_port}`")

bot.run('MTIwMTExMzEyNjcwMDA2MDczMg.Gt54nE.-bTMJhYEo0AQoxlGSDDYFycI_ffbUqcEHpEnsQ')
