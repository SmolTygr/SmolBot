import logging
import os
import discord
from discord.ext import commands
import configparser

# Custom modules
from log import setup_logging, log_command


# Setup Logging
logger = setup_logging()


#Intents
intents = discord.Intents.default()
intents.message_content = True

class SmolBot(commands.Bot):
    
    def __init__(self, prefix: str, intents: discord.Intents, logger: logging.Logger):
        
        # Call commands.Bot __init__
        super().__init__(command_prefix=prefix, intents=intents, logger=logger)
        
        # Store logger here to stop it being parsed to each extension
        self.logger = logger 
        
        # self._config_path stored as used in control.py 'reset_config'
        self._config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self._config_path)
        

if __name__ == '__main__':
    
    token_path = os.path.join(os.path.pardir(__file__), 'token.txt')

    # Get the OATH2 TOKEN to connect bot
    with open(token_path, 'r') as file:
        TOKEN = file.readline()
    
    # Have to create bot instance here, for .command/.event dectorators.
    # An instance is required, as it has to pass "self" into it.
    # See discord.py API on this
    smolbot = SmolBot(prefix='!', intents=intents, logger=logger)
    smolbot.load_extension('clips')
    smolbot.load_extension('control')
    smolbot.load_extension('loose')

    @smolbot.event
    async def on_ready():
        """Perform actions when bot comes online"""
        logger.info('SmolBot is now online!')
    
    smolbot.run(TOKEN)
