import logging
import os
import discord
from discord.ext import commands
import sqlite3

# Custom modules
from log import setup_logging

# Setup Logging
logger = setup_logging()

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

class SmolBot(commands.Bot):

    def __init__(self,
                 prefix: str,
                 intents: discord.Intents,
                 logger: logging.Logger):
        
        # Call commands.Bot __init__
        super().__init__(command_prefix=prefix, intents=intents, logger=logger)
        
        # Store logger here to stop it being parsed to each extension
        self.logger = logger
        self.smol_tygr = None  # Set on_ready() event.
        
    def connect_to_database(self):
        """Attempt to connect to the local bot database"""
        
        # Check if the path exists already. Ensures we know nothing weird has
        # happened to the database. Otherwise sqlite3.connect will simply make
        # a new database. 
        db_path = os.path.join(os.path.dirname(__file__), 'SmolDB.db')
        if not os.path.exists(db_path):
            raise OSError('Could not find the SmolDB.db file')

        try:
            self.db_connection = sqlite3.connect(db_path)
            self.db_cursor = self.db_connection.cursor()
        except:
            raise RuntimeError('Cannot connect to SQLite Database')

    async def on_ready(self):
        """Perform actions when bot comes online"""
        # Using fetch_user as get_user requires the user to be in the cache.
        self.smol_tygr =  await self.fetch_user(325726203681964043)
        
        await self.tree.sync(guild=discord.Object(id=1016382572776915094)) 
        
        logger.info('SmolBot is now online!')
        

    async def setup_hook(self):
        
        # List of Cogs to load. Note they are loaded in order. Always load the
        # errors one first, to ensure any internal errors are recorded on
        # the logs. Otherwise they are suprressed
        cogs_to_load = ['cogs.Errors', 'cogs.AdminControls']
        
        for cog in cogs_to_load:
            await self.load_extension(cog)
            
        self.connect_to_database()
        



if __name__ == '__main__':
    
    # Get the OATH2 TOKEN to connect bot
    with open(os.path.join(os.path.dirname(__file__), 'anti_token.txt'), 'r') as file:
        TOKEN = file.readline()
    
    # Have to create bot instance here, for .command/.event dectorators.
    # An instance is required, as it has to pass "self" into it.
    # See discord.py API on this
    smolbot = SmolBot(prefix='?', intents=intents, logger=logger)


    # @smolbot.command()
    # async def borby(ctx):
    #     if ctx.message.author.id == 325726203681964043:
    #         await ctx.message.reply('Raising error!')
    #         raise RuntimeError('Oh no, it is borby')
    #     else:
    #         await ctx.message.reply('no! No borby command for you >:(')
            
    # @smolbot.event 
    # async def on_mesage(message):

    #     smolbot.logger.info('Message: %s', message.content)
    #     if message.content.contains('1039537679882276904'):
    #         await message.channel.send("We don't allow that emote in here...")
    #         await message.delete()

    @smolbot.command()
    async def raise_error(ctx):
        raise ValueError('Oh no')

    smolbot.run(TOKEN, log_handler=None)