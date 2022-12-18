import os
import discord
from discord.ext import commands
from discord import app_commands

with open(os.path.join(os.path.dirname(__file__), 'anti_token.txt'), 'r') as file:
        TOKEN = file.readline()


class Confirm(discord.ui.View):
    def __init__(self, option_one, option_two):
        super().__init__(timeout=None)
        self.value = None
        self.option_one = option_one 
        self.option_two = option_two
        
    @discord.ui.button(label=f' ', style=discord.ButtonStyle.gray, custom_id='poll:o1', emoji='🎥')
    async def name_one(self, interaction, button):
        await poll_results(interaction=interaction, option=self.option_one)      

    @discord.ui.button(label=' ', style=discord.ButtonStyle.gray, custom_id='poll:o2', emoji='🧼')
    async def name_two(self, interaction, button):
        await poll_results(interaction=interaction, option=self.option_two)


async def poll_results(interaction, option):
    """Set a user role in a server"""
    print(option)
    bot = interaction.client
    bot.results[option] += 1
    print(bot.results)
    await interaction.response.send_message(f'Choice added!', ephemeral=True)
        
# Intents
intents = discord.Intents.default()
intents.message_content = True

class AntiBirdyBot(commands.Bot):

    def __init__(self, prefix: str, intents: discord.Intents):
        # Call commands.Bot __init__
        super().__init__(command_prefix=prefix, intents=intents)
        self.results = {}

    async def on_ready(self):
        """Perform actions when bot comes online"""
        # Using fetch_user as get_user requires the user to be in the cache.
        print('alive')
        await self.tree.sync(guild=discord.Object(id=1016382572776915094))
    
bot = AntiBirdyBot(prefix = ';', intents=intents)
   
@bot.tree.command(name='test', description='A simple test command',
                  guild=discord.Object(id=1016382572776915094))
@app_commands.describe(name='Please tell me your name!')
async def self(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f'Hello {name} i am AntiBirdyBot')
    

@bot.tree.command(name='poll', description='Create a simple poll', guild=discord.Object(id=1016382572776915094))
async def poll(interaction: discord.Interaction, option_one: str, option_two: str):
    
    interaction.client.results[option_one] = 0
    interaction.client.results[option_two] = 0 
        
    user_name = interaction.user.display_name
    embed = discord.Embed(title=f"Poll created by {user_name}\t\t\t\t ",
                              description="Poll description",
                              color=0xFFC0CB)
    
    embed.add_field(name=f"🎥 {option_one}", value="Option one", inline=False)
    embed.add_field(name=f"🧼 {option_two}", value="Option two", inline=False)
    
    await interaction.response.send_message(embed=embed, view=Confirm(option_one=option_one, option_two=option_two))

@bot.tree.context_menu(name='Show Join Date', guild=discord.Object(id=1016382572776915094))
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

bot.run(TOKEN)


