import logging
import os
import discord
from discord.ext import commands
import configparser

from roles import roles

# Custom modules
from sql import database_connect
from log import setup_logging


# Setup Logging
logger = setup_logging()


# Intents
intents = discord.Intents.default()
intents.message_content = True


class SmolBot(commands.Bot):

    def __init__(self, prefix: str, intents: discord.Intents, logger: logging.Logger):

        # Call commands.Bot __init__
        super().__init__(command_prefix=prefix, intents=intents, logger=logger)

        # Store logger here to stop it being parsed to each extension
        self.logger = logger
        
        self.smol_user = None  # Set on_ready() event.
    
        # self._config_path stored as used in control.py 'reset_config'
        self._config_path = os.path.join(
            os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self._config_path)
        
        # Connect to database
        self.databse = database_connect(os.path.join(os.path.dirname(__file__), 'smolbot.sqlite'))

    async def setup_hook(self):
        await self.load_extension('clips')
        await self.load_extension('control')
        await self.load_extension('loose')
        
        await self.add_cog(roles(self))

if __name__ == '__main__':

    token_path = os.path.join(os.path.dirname(__file__), 'token.txt')

    # Get the OATH2 TOKEN to connect bot
    with open(token_path, 'r') as file:
        TOKEN = file.readline()

    # Have to create bot instance here, for .command/.event dectorators.
    # An instance is required, as it has to pass "self" into it.
    # See discord.py API on this
    smolbot = SmolBot(prefix='!', intents=intents, logger=logger)
    

    @smolbot.event
    async def on_ready():
        """Perform actions when bot comes online"""
        # Using fetch_user as get_user requires the user to be in the cache.
        smolbot.smol_user =  await smolbot.fetch_user(int(325726203681964043))
        logger.info('SmolBot is now online!')

    @smolbot.event
    async def on_command_error(ctx, error):
        """Method to manage errors inside Cog"""
        smolbot.logger.error('SmolBot Error : Command "%s" : Server "%s" : Channel: "%s" : User "%s" : %s', ctx.command, ctx.guild.name, ctx.channel.name,  ctx.author.name, error)
        await smolbot.smol_user.send(f'SmolBot Error : Command {ctx.command} : Server {ctx.guild.name} : Channel: {ctx.channel.name} : User {ctx.author.name} : {error}')
        
    # @smolbot.command()
    # async def ask(ctx: commands.Context):
    #     await ctx.send('...', view=Confirm())

    smolbot.run(TOKEN, log_handler=None)
