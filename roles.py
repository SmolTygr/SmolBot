import logging

import discord
from discord.ext import commands
from log import log_command

class roles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role_embed(self, ctx):
        embed = discord.Embed(title="Choose your role\t\t\t\t ",
                              description="",
                              color=0xFFC0CB)
        
        embed.add_field(name="🎥 Go Live",
                        value="Get pinged when Smol goes live\n",
                        inline=False)
        
        embed.add_field(name="🍆🧼 Soapy Boys",
                        value="Get Soapy and have access to the NSFW channel\n",
                        inline=False)

        embed.add_field(name="🤖 Bot Lovers",
                        value="View all the SmolBot related channels\n",
                        inline=False)       
                
        embed.set_footer(text='For any questions please ask: SmolTygr')
        await ctx.message.channel.send(embed=embed, view=Confirm())
        

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        
    @discord.ui.button(label=' Go Live', style=discord.ButtonStyle.gray, custom_id='persistent_view:golive', emoji='🎥')
    async def live(self, interaction, button):
        await set_role(interaction=interaction, role_name='GoLive')      

    @discord.ui.button(label=' Get Soapy', style=discord.ButtonStyle.gray, custom_id='persistent_view:soap', emoji='🍆🧼')
    async def soap(self, interaction, button):
        await set_role(interaction=interaction, role_name='Soapy Boys')
        
    @discord.ui.button(label=' Gimme Bots', style=discord.ButtonStyle.gray, custom_id='persistent_view:bots', emoji='🤖')
    async def bot(self, interaction, button):
        await set_role(interaction=interaction, role_name='Bot Lovers')    

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