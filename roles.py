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
        
    @discord.ui.button(label=' Soapy', style=discord.ButtonStyle.green, custom_id='persistent_view:role', emoji='🧼')
    async def role(self, interaction, button):
        await set_role(interaction=interaction, role_name='Soaps')      

    @discord.ui.button(label=' Tiger', style=discord.ButtonStyle.green, custom_id='persistent_view:role', emoji='🐯')
    async def role(self, interaction, button):
        await set_role(interaction=interaction, role_name='Tigers')    

async def set_role(interaction, role_name):
    """Set a user role in a server"""
    
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role, reason='Click the role button')
        await interaction.response.send_message(f'You have been removed from the role: {role_name}', ephemeral=True)
    
    else:
        await interaction.user.add_roles(role, reason='Clicked the roll button')
        await interaction.response.send_message(f'You have been added to the role: {role_name}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(roles(bot))