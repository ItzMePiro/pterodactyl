import discord
from discord.ext import commands
import paramiko
import random
import string

# Define intents
intents = discord.Intents.default()

# Discord Bot setup with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to create random SSH password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to create VPS container using Docker
def create_vps_container(user_id):
    # Connect to your VPS via SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('your_vps_ip', username='your_ssh_username', password='your_ssh_password')

    # Generate random SSH port
    ssh_port = random.randint(10000, 20000)

    # Generate random password
    ssh_password = generate_password()

    # Execute Docker command to create container
    container_id = f"container_{user_id}_{random.randint(1000, 9999)}"
    docker_command = f'docker run -d -p {ssh_port}:22 --name {container_id} ubuntu'
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(docker_command)

    # Close SSH connection
    ssh_client.close()

    return ssh_port, ssh_password, container_id

# Function to execute commands on VPS
def execute_command_on_vps(command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('your_vps_ip', username='your_ssh_username', password='your_ssh_password')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(command)
    output = ssh_stdout.read().decode()
    ssh_client.close()
    return output

# Command to create VPS container
@bot.command()
async def create(ctx):
    # Create VPS container
    ssh_port, ssh_password, container_id = create_vps_container(ctx.author.id)

    # Send SSH information via DM
    await ctx.author.send(f"Your VPS container has been created.\n"
                          f"SSH Port: {ssh_port}\n"
                          f"SSH Password: {ssh_password}\n"
                          f"Container ID: {container_id}")

# Command to execute custom command on VPS
@bot.command()
async def execute(ctx, *, command):
    # Execute command on VPS
    output = execute_command_on_vps(command)

    # Send output via DM
    await ctx.author.send(f"Command executed:\n```{command}```\nOutput:\n```{output}```")

# Bot token
TOKEN = 'your_discord_bot_token_here'

# Run the bot
bot.run(TOKEN)
                         
