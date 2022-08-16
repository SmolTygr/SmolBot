from logging import handlers
import os
import discord
from discord.ext import commands
import random
import logging
from logging import handlers
import configparser

# Constants / global variables
LOG_BACKUP_COUNT = 5
LOG_NAME = 'smolLog.log'
CONFIG_NAME = 'smolConfig.ini'
DIR_ = os.path.dirname(__file__)
BOT_PREFIX = '!'

# Get command / config settings
config_path = os.path.join(DIR_, CONFIG_NAME)
config = configparser.ConfigParser()
config.read(config_path)

# Setup logging
logger = logging.getLogger('SmolBot')
logger.setLevel(logging.DEBUG)

# All-purpose formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

# File handler
file = handlers.RotatingFileHandler(filename=os.path.join(DIR_, LOG_NAME),
                                    mode='a',
                                    encoding='UTF-8',
                                    backupCount=LOG_BACKUP_COUNT)
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)
logger.addHandler(file)    

# Have to create bot instance here, for .command/.event dectorators.
# An instance is required, as it has to pass "self" into it.
# See discord.py API on this
smolbot = commands.Bot(command_prefix=BOT_PREFIX, logger=logger)

#TODO: Rewrite as a wrapper function.
def log_command(ctx, command_name: str, *, level: int = logging.DEBUG):
    """Basic logging for when a user calls a command"""
    logger.log(level=level, msg='%s called: "%s"' %
               (str(ctx.author), command_name))

@smolbot.event
async def on_ready():
    """Perform actions when bot comes online"""
    logger.info('SmolBot is now online!')
    
@smolbot.command(name='ping')
async def _(ctx):
    """Ping smolbot to check its status"""
    log_command(ctx, 'ping')
    await ctx.message.reply(config['ping']['response'])


@smolbot.command(name='bois')
async def _(ctx):
    """Respond with a link to SydneyMGames clip"""
    log_command(ctx, 'bois')
    embed = discord.Embed(**config['bois'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='scuse')
async def _(ctx):
    """Respond with a link to SydneyMGames clip"""
    log_command(ctx, 'scuse')
    embed = discord.Embed(**config['scuse'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='dolphin')
async def _(ctx):
    """Respond with a link to BirdyRage clip"""
    log_command(ctx, 'dolphin')
    embed = discord.Embed(**config['dolphin'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='brenky')
async def _(ctx):
    """Respond with a link to BirdyRage clip"""
    log_command(ctx, 'brenky')
    embed = discord.Embed(**config['brenky'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='batman')
async def _(ctx):
    """Respond with a link to BirdyRage clip"""
    log_command(ctx, 'batman')
    embed = discord.Embed(**config['batman'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='soap')
async def _(ctx):
    """Respond with a link to BirdyRage clip"""
    log_command(ctx, 'soap')
    embed = discord.Embed(**config['soap'])
    await ctx.message.reply(embed=embed)


@smolbot.command(name='reset_config')
async def _(ctx):
    log_command(ctx, 'reset_config')
    
    allowed_users = config['reset_config']['allowed_users'].split(sep=', ')
    if str(ctx.author)[:-5] not in allowed_users:
        await ctx.send('You do not have the power! You cannot reset me. Muhahaha')
        await ctx.message.add_reaction('❎')
        return 
        
    config.read(config_path)
    logger.info('Config.ini re-read!')
    await ctx.message.add_reaction('✅')


@smolbot.command(name='smol_help')
async def _(ctx):
    log_command(ctx, 'smol_help')
    message = """Hello, I am a very smol bot (🤖), you can call me SmolBot.
    
Currently, these are the commands you can call:
    !smol help - This command :)
    !bois - Link to Sydney's clip
    !scuse - Link to another Sydney clip
    !ping - Check i am awake
    !ciri - Get a random picture of Ciri
    !cool - Find out how cool you are
    !suggest - Send a suggestion for a change to SmolBot
    
If you have questions / issues, just let SmolTygr know.
"""
    await ctx.message.reply(message)

@smolbot.command(name='ciri')
async def _(ctx):
    log_command(ctx, 'ciri')
    
    # Get a random .png from Ciri folder
    images = os.listdir(os.path.join(DIR_, 'ciri'))
    images = [file for file in images if file.endswith('.png')]
    
    random_image = images[random.randint(0, len(images)-1)]
    random_image_path = os.path.join(DIR_, 'ciri', random_image)
    
    file = discord.File(random_image_path, 'ciri.png')
    embed = discord.Embed(author='Smol',
                          title='Ciri',
                          description='Have a free ciri photo!')
    embed.set_image(url="attachment://ciri.png")
    await ctx.message.reply(file=file, embed=embed)

@smolbot.command(name='cool')
async def _cool(ctx):
    log_command(ctx, 'cool')

    if str(ctx.author)[:-5] == 'Smol_Tygr':
        await ctx.send('Smol is the coolest. No need to even check')
        return None

    coolness = random.randint(0, 101)
    message = "Function has broken. Balls."

    if coolness < 10:
        message = "Oh... Maybe don't let people know this"
    elif coolness < 30:
        message = "That's not very cool"
    elif coolness < 50:
        message = "Please try again, but harder"
    elif coolness < 70:
        message = "That's not bad!"
    elif coolness < 90:
        message = "Pretty damn cool!"
    elif coolness < 101:
        message = "So cool!"
    elif coolness == 101:
        message = "THE COOLEST."

    await ctx.send(f'{str(ctx.author)[:-5]} is {coolness}% cool. {message}')


@smolbot.command(name='suggest')
async def _(ctx):
    log_command(ctx, 'suggest')

    # Suggestion / idea chnnael on A Smol Server
    channel = smolbot.get_channel(1008099482229031042)

    # Strip first part of message which is !suggest
    message = str(ctx.message.content)[9:]
    await channel.send(f'{ctx.author.mention} has suggested: {message}')
    await ctx.message.reply('Thank you for the suggestion. It has been sent to A Smol Server')




# @smol_bot.listen('on_message')
# async def on_message_(message):

#     # Ignore messages from the bot itself.
#     if message.author == smol_bot.user:
#         return


if __name__ == '__main__':
    token_path = os.path.join(DIR_, 'token.txt')
    
    # Get the OATH2 TOKEN to connect bot
    with open(token_path, 'r') as file:
        TOKEN = file.readline()
     
    smolbot.run(TOKEN)
