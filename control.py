from discord.ext import commands
from discord import ChannelType

# Custom module import
from log import log_command


class control(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # Check documentation: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.check
    def _smoltygr_check():
        def predicate(ctx):
            return ctx.message.author.id == 325726203681964043
        return commands.check(predicate)
    
    def _server_owner_check():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)
    
    @commands.command()
    @commands.check_any(_smoltygr_check())
    async def reset_config(self, ctx):
        log_command(ctx, self.bot.logger, 'reset_config')

        self.bot.config.read(self.bot._config_path)
        self.bot.logger.info('Config.ini re-read!')
        await ctx.message.add_reaction('✅')
        
    @commands.command()
    @commands.check_any(_smoltygr_check())
    async def reload_ex(self, ctx):
        log_command(ctx, self.bot.logger, 'reload_ex')
        for extension in self.bot.config['reload_ex']['names'].split(sep=', '):
            await self.bot.reload_extension(extension)

        await ctx.message.add_reaction('✅')
            
    @commands.command()
    async def ping(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('👍')
        
        
    @commands.command(aliases=['suggestion'])
    async def suggest(self, ctx):
        """Creates a thread in Suggestion channel"""
        log_command(ctx,  self.bot.logger, 'suggest')

        # Get the A Smol Server - Suggestion channel
        channel = self.bot.get_channel(1008099482229031042)
        thread = await channel.create_thread(name=f'{str(ctx.author.display_name)} suggestion',
                                             type=ChannelType.public_thread)

        await thread.send(f'<@325726203681964043>, there is a new suggestion from {ctx.message.author.mention}.')
        await thread.send(str(ctx.message.content)[9:])
        await ctx.message.reply(f'Thank you for the suggestion. A thread has been made {thread.mention}')
        
    @commands.command()
    async def smol_help(self, ctx):
        log_command(ctx,  self.bot.logger, 'smol_help')
        message = """Hello, I am a very smol bot (🤖), you can call me SmolBot.
        
        Currently, these are the commands you can call:
            !smol help - This command :)
            !clips - Get a list of great twitch clips commands
            !ping - Check i am awake
            !ciri - Get a random picture of Ciri
            !cool - Find out how cool you are
            !good_bot / bad_bot - Tell the bot how you feel
            !suggest - Send a suggestion for a change to SmolBot
            
        If you have questions / issues, just let SmolTygr know.
        """
        await ctx.message.reply(message)
        

async def setup(bot):
    await bot.add_cog(control(bot))
