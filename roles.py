import logging

import discord
from discord.ext import commands
from log import log_command

class roles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command()
    async def role_embed(self, ctx):
        embed = discord.Embed(title="Choose your role", description="", color=0xFFC0CB)
        embed.add_field(name="🐯 Tiger Role", value="Be a smol tiger", inline=False)
        embed.add_field(name="🧼 Soap Role", value="Be a soap boy", inline=False)
        
        
        embed.set_footer(text='For any questions please ask: SmolTygr')
        await ctx.message.channel.send(embed=embed, view=Confirm())
        

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        
    @discord.ui.button(label='Role', style=discord.ButtonStyle.green, custom_id='persistent_view:role', emoji='🧼')
    async def role(self, interaction, button):
        role = discord.utils.get(interaction.guild.roles, name='Test')
        await interaction.user.add_roles(role, reason='Clicked the roll button')
        await interaction.response.send_message('This is green', ephemeral=True)


async def setup(bot):
    await bot.add_cog(roles(bot))