import discord
from discord.ext import commands


class Errors(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener("on_error")
    async def on_error(self, event, *args, **kwargs):
        """Handle python errors (not command or app_command errors)"""
        self.bot.logger.error(('Internal Error: Event %s : Args %s ' 
                               ': kwargs %s'),
                               event,
                               args, 
                               kwargs,
                               exc_info=True)
    
    async def on_command_error(self, ctx, error):
        """Management of command errors"""
        
        # Handle users requesting a command that does not exist
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.reply(("Sorry i don't know that command.\n\n"
                                     "Use !help for a list of all commands."
                                     "\n \nThis message auto-deletes in 30 "
                                     "seconds"),
                                    delete_after=30)
            return
        
        # Handle users who fail a predicate check (not appropirate permission)
        if isinstance(error, commands.CheckFailure):
             await ctx.message.reply(("Sorry, you do not have the appropirate"
                                      "permissions to use this command.\n\n"
                                      "If you think this is a mistake, please "
                                      "contact the server owner or SmolTygr."
                                      "\n\nThis message will auto-delete in "
                                      "30 seconds."),
                                    delete_after=30)
             return           
        
        # Record the error and traceback in the logs
        self.bot.logger.error(('SmolBot Error : Command "%s" : Server "%s' 
                               ': Channel: "%s" : User "%s" : %s'),
                               ctx.command,
                               ctx.guild.name,
                               ctx.channel.name,
                               ctx.author.name,
                               error,
                               exc_info=True)
        
        # Reply to the user
        await ctx.message.reply((f'Sorry this command has failed. SmolTygr  '
                                 'has been told about it.\n \nThis message '
                                 'will auto-delete in 30 seconds'),
                                delete_after=30)
        
        # Generate the embed "error log" to send to SmolTygr
        embed = discord.Embed(title='🐛 Report', description='')
        
        embed.add_field(name="Command",
                        value=f"{ctx.command}",
                        inline=False)
        
        embed.add_field(name="Server",
                        value=f"{ctx.guild.name}",
                        inline=False)
        
        embed.add_field(name="Channel",
                        value=f"{ctx.channel.name}",
                        inline=False)
        
        embed.add_field(name="User",
                        value=f"{ctx.author.name}",
                        inline=False)
        embed.add_field(name="Error",
                        value=f"{error}",
                        inline=False)
        
        # Send SmolTygr a DM with information directly
        await self.bot.smol_tygr.send('', embed=embed)
        
    async def on_app_command_error(self, interaction, error):
        reply = interaction.response.send_message
        
        # Record the error and traceback in the logs
        self.bot.logger.error(('SmolBot Error : Command "%s" : Server "%s' 
                               ': Channel: "%s" : User "%s" : %s'),
                               interaction.command.name,
                               interaction.guild.name,
                               interaction.channel.name,
                               interaction.user.name,
                               error,
                               exc_info=True)
        
        # Send message to user to warn them of the failure
        await reply((f'Sorry this command has failed. SmolTygr has been told '
                     'about it.\n \nThis message will auto-delete in 30 '
                     'seconds'),
                    delete_after=30)
        
        # Generate the embed "error log" to send to SmolTygr
        embed = discord.Embed(title='🐛 Report', description='')
        
        embed.add_field(name="Command",
                        value=f"{interaction.command.name}",
                        inline=False)
        
        embed.add_field(name="Server",
                        value=f"{interaction.guild.name}",
                        inline=False)
        
        embed.add_field(name="Channel",
                        value=f"{interaction.channel.name}",
                        inline=False)
        
        embed.add_field(name="User",
                        value=f"{interaction.user.name}",
                        inline=False)
        embed.add_field(name="Error",
                        value=f"{error}",
                        inline=False)
        
        # Send SmolTygr a DM with information directly
        await self.bot.smol_tygr.send('', embed=embed)
        
async def setup(bot):
    await bot.add_cog(Errors(bot))