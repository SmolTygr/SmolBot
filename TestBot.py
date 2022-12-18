import os
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class AntiBirdyBot(commands.Bot):

    def __init__(self, prefix: str, intents: discord.Intents):
        # Call commands.Bot __init__
        super().__init__(command_prefix=prefix, intents=intents)


    async def on_ready(self):
        """Perform actions when bot comes online"""
        
        # Get a connection to the database
        try:
            self.db_connection = sqlite3.connect('testdb.db')
            self.db_cursor = self.db_connection.cursor()
        except:
            raise RuntimeError('Cannot connect to Bot Database')
        
        await self.tree.sync(guild=discord.Object(id=1016382572776915094))
        print('AntiBirdyBot O N L I N E')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
bot = AntiBirdyBot(prefix = ';', intents=intents)

@bot.tree.command(name='setserveradmin',
                  description='Set a user as a server admin for BOT related work',
                  guild=discord.Object(id=1016382572776915094))
@app_commands.describe(name="The text part of the user's name",
                       number="The 4-digit number of the user")
async def SetServerAdmin(interaction: discord.Interaction,
                         name: str,
                         number: str):
    
    # To do: ADMIN check function
    
    server_id = interaction.guild_id
    
    # First check that the user exists at all
    server = bot.get_guild(server_id)
    
    user = server.get_member_named(f'{name}#{number}')
    if user is None:
        await interaction.response.send_message(('Error: Could not find the user'
                                                 'in the server. Please check the '
                                                 'details and try again.'),
                                                ephemeral=True)
        
        user = server.get_member_named('Smol_Tygr#7672')
        print('oh no')
        return 
    
    # Ensure DB is up-to-date before checking things
    bot.db_cursor.execute(f"""SELECT * 
                              FROM ServerAdmins
                              WHERE ServerAdmins.ServerID="{server_id}" 
                              AND ServerAdmins.UserID="{user.id}"
                          """)
        
    # If this returns anything but a None then User already in DB
    if bot.db_cursor.fetchone():
        await interaction.response.send_message(('User already has admin'
                                                 'bot rights for this server.'),
                                                ephemeral=True)

    elif bot.db_cursor.fetchone() is None:
        bot.db_cursor.execute(f"""
                              INSERT INTO ServerAdmins VALUES
                              (NULL, {server_id}, {user.id})""")
        bot.db_connection.commit()

        await interaction.response.send_message(('User now has admin'
                                                 'bot rights for this server. !yay'),
                                                ephemeral=True)

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'anti_token.txt'), 'r') as file:
            TOKEN = file.readline()

    bot.run(TOKEN)