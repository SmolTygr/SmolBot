import logging

import discord
from discord.ext import commands
from log import log_command

class roles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command()
    async def role_embed(self, ctx):
        embed = discord.Embed(title="Choose your role", description="beep boop", color='xx') #,color=Hex code
        embed.add_field(name="Name", value="you can make as much as fields you like to")
        await ctx.message.channel.send(embed=embed)
        
    async def cog_command_error(self, ctx, error):
        """Method to manage errors inside Cog"""
        self.bot.logger.error('Error inside commands cog: %s', error)
        await self.smol_user.send(f'An error has occured in SmolBot TestCog: {error}')
        

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        
    @discord.ui.button(label='Role', style=discord.ButtonStyle.green, custom_id='persistent_view:role')
    async def role(self, interaction, button):
        await interaction.response.send_message('This is geen', ephemeral=True)
        
        

