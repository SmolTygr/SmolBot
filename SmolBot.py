
import os
import discord
from discord.ext import commands
import random
import configparser

# Custom modules
from log import setup_logging, log_command
import clips


# Constants / global variables
CONFIG_NAME = 'smolConfig.ini'
DIR_ = os.path.dirname(__file__)
BOT_PREFIX = '!'

# Setup Logging
logger = setup_logging()

# Get command / config settings
config_path = os.path.join(DIR_, CONFIG_NAME)
config = configparser.ConfigParser()
config.read(config_path)

# Have to create bot instance here, for .command/.event dectorators.
# An instance is required, as it has to pass "self" into it.
# See discord.py API on this
smolbot = commands.Bot(command_prefix=BOT_PREFIX, logger=logger)
smolbot.add_cog(clips.Clips(bot=smolbot, config=config))


@smolbot.event
async def on_ready():
    """Perform actions when bot comes online"""
    logger.info('SmolBot is now online!')


@smolbot.command(name='ping')
async def _(ctx):
    """Ping smolbot to check its status"""
    log_command(ctx, 'ping')
    await ctx.message.reply(config['ping']['response'])


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


@smolbot.command(name='clips')
async def _(ctx):
    """Send a list of clip commands"""
    log_command(ctx, 'clips')

    message = """Some amazing clips from the best streamers:
        !bois
        !scuse
        !brenky
        !dolphin
        !batman
        !soap
        !blow
        !bwah
        
    If you want a random one:
        !random_clip
    """
    await ctx.message.reply(message)


@smolbot.command(name='smol_help')
async def _(ctx):
    log_command(ctx, 'smol_help')
    message = """Hello, I am a very smol bot (🤖), you can call me SmolBot.
    
Currently, these are the commands you can call:
    !smol help - This command :)
    !clips - Get a list of great twitch clips commands
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
