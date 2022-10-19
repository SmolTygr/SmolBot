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
        self.client = discord.Client(intents=intents)
        self.smol_user = self.client.get_user(325726203681964043)

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
        logger.info('SmolBot is now online!')
        
    @smolbot.command
    async def test_dm(ctx):
        smolbot.logger.info('Test dm called')
        raise AttributeError('test error')
        await smolbot.smol_user.send(f'An error has occured in SmolBot TestCog:')
        
        
    @smolbot.event
    async def on_command_error(ctx, error):
        """Method to manage errors inside Cog"""
        smolbot.logger.error('Error inside SmolBot: %s', error)
        await smolbot.smol_user.send(f'An error has occured in SmolBot: {error}')
        
    # @smolbot.command()
    # async def ask(ctx: commands.Context):
    #     await ctx.send('...', view=Confirm())

    smolbot.run(TOKEN, log_handler=None)
