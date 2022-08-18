from discord.ext import commands

# Custom module import
from log import log_command


class control(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def reset_config(self, ctx):
        log_command(ctx, self.bot.logger, 'reset_config')

        allowed_users = self.bot.config['reset_config']['allowed_users'].split(sep=', ')
        if str(ctx.author)[:-5] not in allowed_users:
            await ctx.send('You do not have the power! You cannot reset me. Muhahaha')
            await ctx.message.add_reaction('❎')
            return

        self.config.read(self.bot._config_path)
        self.bot.logger.info('Config.ini re-read!')
        await ctx.message.add_reaction('✅')
        
    @commands.command()
    async def reload_ex(self, ctx):
        log_command(ctx, self.bot.logger, 'reload_ex')
        for extension in self.bot.config['reset_config']['extension_names'].split(sep=', '):
            await self.bot.reload_extension(extension)

        await ctx.message.add_reaction('✅')
            
            
    @commands.command(name='ping')
    async def _(self, ctx):
        """Ping smolbot to check its status"""
        log_command(ctx, self.bot.logger, 'ping')
        await ctx.message.add_reaction('👍')
        
        
    @commands.command(aliases=['suggestion'])
    async def suggest(self, ctx):
        log_command(ctx,  self.bot.logger, 'suggest')

        # Suggestion / idea chnnael on A Smol Server
        channel = self.bot.get_channel(1008099482229031042)

        # Strip first part of message which is !suggest
        message = str(ctx.message.content)[9:]
        await channel.send(f'{ctx.author.mention} has suggested: {message}')
        await ctx.message.reply('Thank you for the suggestion. It has been sent to A Smol Server')
        
    
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
            !suggest - Send a suggestion for a change to SmolBot
            
        If you have questions / issues, just let SmolTygr know.
        """
        await ctx.message.reply(message)
        

async def setup(bot):
    await bot.add_cog(control(bot))
