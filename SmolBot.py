import logging
import os
import discord
from discord.ext import commands
import configparser

from roles import Confirm

# Custom modules
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
        

    async def setup_hook(self):
        await self.load_extension('clips')
        await self.load_extension('control')
        await self.load_extension('loose')
        await self.load_extension('roles')
        
        self.add_view(Confirm())  # message_id=###


if __name__ == '__main__':
    
    # Get the OATH2 TOKEN to connect bot
    with open(os.path.join(os.path.dirname(__file__), 'token.txt'), 'r') as file:
        TOKEN = file.readline()
    
    # Have to create bot instance here, for .command/.event dectorators.
    # An instance is required, as it has to pass "self" into it.
    # See discord.py API on this
    smolbot = SmolBot(prefix='!', intents=intents, logger=logger)

    @smolbot.event
    async def on_ready():
        """Perform actions when bot comes online"""
        # Using fetch_user as get_user requires the user to be in the cache.
        smolbot.smol_user =  await smolbot.fetch_user(325726203681964043)
        logger.info('SmolBot is now online!')
        
    @smolbot.command()
    async def borby(ctx):
        raise RuntimeError('Oh no, it is borby')

    @smolbot.event
    async def on_command_error(ctx, error):
        """Method to manage errors inside SmolBot"""
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.reply(f"Sorry i don't know that command.\n \nUse !help for a list of all commands.\n \nThis message auto-deletes in 30 seconds",
                                    delete_after=30)
            return
        
        # Record the error and traceback in the logs
        smolbot.logger.error('SmolBot Error : Command "%s" : Server "%s" : Channel: "%s" : User "%s" : %s', ctx.command, ctx.guild.name, ctx.channel.name,  ctx.author.name, error, exc_info=True)
        
        # Reply to the user
        await ctx.message.reply(f'Sorry this command has failed. SmolTygr has been told about it.\n \nThis message will auto-delete in 30 seconds', delete_after=30)
        
        # Send SmolTygr a DM with information directly
        await smolbot.smol_user.send(f'SmolBot error in "{ctx.command}"\n{ctx.guild.name} - {ctx.channel.name}\nCalled by "{ctx.author.name}"\n \n{error}')


    smolbot.run(TOKEN, log_handler=None)