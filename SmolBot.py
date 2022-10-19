import logging
import os
import discord
from discord.ext import commands
import configparser

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


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()        

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
        
        
    @smolbot.command()
    async def ask(ctx: commands.Context):
        
        view = Confirm()
        await ctx.send('Question?', view=view)
        await view.wait()
        
        if view.value is None:
            print('Time out')
        elif view.value:
            print('Conf')
        else:
            print('cancelled')

    smolbot.run(TOKEN, log_handler=None)
