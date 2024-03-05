import discord
from discord.ext import commands
import subprocess
import random
import string

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to generate a random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Function to create a Docker container with custom port and password
def create_container(container_name):
    try:
        ssh_port = random.randint(49152, 65535)  # Generate random port in ephemeral port range
        password = generate_password()

        # Create container with custom port mapping and password
        subprocess.run(['docker', 'run', '-d', '--name', container_name, '-p', f'{ssh_port}:22', '-e', f'SSH_PASSWORD={password}', 'ubuntu'])
        
        # Return container info (name, port, password)
        return container_name, ssh_port, password
    except Exception as e:
        print(f"Error creating container: {e}")
        return None

# Command to create a container
@bot.command()
async def create(ctx, container_name):
    container_info = create_container(container_name)
    if container_info:
        name, port, password = container_info
        await ctx.send(f"Container {name} created successfully!\nSSH Port: {port}\nSSH Password: {password}")
    else:
        await ctx.send(f"Failed to create container {container_name}. Please try again.")

# Run the bot
bot.run('YOUR_DISCORD_TOKEN')
