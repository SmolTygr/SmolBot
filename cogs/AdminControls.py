import discord
from discord.ext import commands
from discord import app_commands 
from typing import Optional

# Custom module import
from log import log_command


class AdminControls(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # Check documentation: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.check
    def smoltygr_check():
        """Check the user is SmolTygr"""
        def predicate(ctx):
            return ctx.message.author.id == 325726203681964043
        return commands.check(predicate)
    
    def server_owner_check(): 
        """Check the user is the server owner"""
        def predicate(ctx):           
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    def server_admin_check():
        """Check the user is a bot server admin in the database"""
        def predicate(ctx):
            bot = ctx.bot                      
            bot.db_cursor.execute(f"""
                                  SELECT
                                    SAD.UserID
                                  FROM 
                                    ServerAdmins AS SAD
                                  WHERE 
                                    SAD.ServerID={ctx.guild.id} 
                                  """)
            admin_ids = [row[0] for row in bot.db_cursor.fetchall()]
            return str(ctx.author.id) in admin_ids
        return commands.check(predicate)
    
    @commands.command()
    @commands.check(smoltygr_check())
    async def sync(self, ctx, setting: Optional[str] =''):
        """Perform bot app_command sync"""
        await ctx.send('Starting SmolBot tree sync', delete_after=60)
        
        # Sync to current guild only
        if setting == '~':
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        
        # Copy all global app commands to current guild
        elif setting == '*':
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        
        # Clear all commands from the current guild and then sync
        elif setting == '^':
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []            
        
        # Default to a global sync
        else:
            synced = await ctx.bot.tree.sync()
        
        # Determine which message to send the user
        if setting == '':
            message = f'Synced {len(synced)} commands globally'
        else:
            message = f'Synced {len(synced)} commands to this server'

        await ctx.send(message)       

    @app_commands.command(name='server_admin',
                          description=('Set a user to be an SmolBot admin in '
                                       'for this server. (All channels)'))
    @app_commands.describe(name="User's name",
                           number="The 4-digit number of the user")
    @commands.check_any(server_admin_check())
    async def SetServerAdmin(self, 
                             interaction: discord.Interaction,
                             name: str,
                             number: str):
        
        server = interaction.guild
        user = server.get_member_named(f'{name}#{number}')
        reply = interaction.response.send_message
        
        # Check to ensure the user actually exists at all
        if user is None: 
            await reply(('Error: Could not find the user in the server.\n\n '
                         'Please check the details and try again.'),
                        ephemeral=True)
            return 
        
        try:
            print('dong')
            # Check the user is not already a server admin
            self.bot.db_cursor.execute(f"""
                                    SELECT *
                                    FROM ServerAdmins AS SAD
                                    WHERE
                                        SAD.ServerID="{str(server.id)}"
                                        AND 
                                        SAD.UserID="{str(user.id)}"
                                    """)
            print('ding')
        except Exception as error:
            print(error)
            await reply(('Error: Could not find the user in the server.\n\n '
                         'Please check the details and try again.'),
                        ephemeral=True)
            
        
        # If this returns anything but a NONE then user already exists in DB
        if self.bot.db_cursor.fetchone():
            await reply('User already has Bot admin rights for this server',
                        ephemeral=True)
            return 
        
        print('ding')
        
        # Add user to DB
        self.bot.db_cursor.execute(f"""
                                   INSERT INTO ServerAdmins
                                   VALUES
                                    (NULL,
                                     {server.id},
                                     {user.id})
                                   """)
        self.bot.db_connection.commit()
        await reply('User now has bot admin rights for this server. !yay',
                    ephemeral=True)

    # @commands.command()
    # @commands.check_any(smoltygr_check())
    # async def reload_ex(self, ctx):
    #     log_command(ctx, self.bot.logger, 'reload_ex')
    #     for extension in self.bot.config['reload_ex']['names'].split(sep=', '):
    #         await self.bot.reload_extension(extension)

    #     await ctx.message.add_reaction('✅')
            
    @commands.command()
    async def ping(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('✅')
        
    @commands.command()
    @commands.check(smoltygr_check())
    async def ping_smol(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('✅')
        
    @commands.command()
    @commands.check(server_owner_check())
    async def ping_owner(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('✅')       

    @commands.command()
    @commands.check(server_admin_check())
    async def ping_admin(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('✅')   
     
    # @commands.command()
    # @commands.check_any(smoltygr_check())
    # async def update(self, ctx):
    #     subprocess.Popen('./update.sh')
    #     await ctx.message.send('I am shutting down and updating')
        
        
    # @commands.command(aliases=['suggestion'])
    # async def suggest(self, ctx):
    #     """Creates a thread in Suggestion channel"""
    #     log_command(ctx,  self.bot.logger, 'suggest')

    #     # Get the A Smol Server - Suggestion channel
    #     channel = self.bot.get_channel(1054049483572400179)
    #     thread = await channel.create_thread(name=f'{str(ctx.author.display_name)} suggestion',
    #                                          type=ChannelType.public_thread)

    #     await thread.send(f'<@325726203681964043>, there is a new suggestion from {ctx.message.author.mention}.')
    #     await thread.send(str(ctx.message.content)[9:])
    #     await ctx.message.reply(f'Thank you for the suggestion. A thread has been made {thread.mention}')

async def setup(bot):
    await bot.add_cog(AdminControls(bot))
