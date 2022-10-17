from discord.ext import commands, tasks
from discord import ChannelType
import discord 
import asyncio
import json

# Custom module import
from log import log_command
from sql import execute_query


class control(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.delayed_message.start()

        self.role_message = 1031657954417586186

    # Check documentation: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.check
    def _smoltygr_check():
        def predicate(ctx):
            return ctx.message.author.id == 325726203681964043
        return commands.check(predicate)

    def _server_owner_check():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Guard statement: Ignore reactions added to messages not the role selection message.
        if payload.message_id != self.role_message:
            return

        self.bot.logger.info(f'{payload.emoji.name}')
        await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name='Test'))

    @tasks.loop()
    async def delayed_message(self):
    
        
        next_task = await execute_query(connection=self.bot.database,
                                        query="""SELECT * FROM delayed_messages ORDER BY call_date LIMIT 1""")
        
        # if no remaining tasks, stop the loop
        if next_task is None:
            self.delayed_message.cancel()
            
        await discord.utils.sleep_until(next_task['call_date'])
            
        channel = self.bot.get_channel(1008115016907640905)
        channel.send(next_task['message'])
        
        await execute_query(connection=self.bot.database,
                            query=f'DELETE FROM delayed_messages WHERE id={next_task["id"]};')
    
    @commands.check_any(_smoltygr_check())
    @commands.command()
    async def test_args(self, ctx):
        
        await ctx.reply('What date/time do you want it?')
        
        try:
            date_time = await self.bot.wait_for('message', timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.message.channel.send(f'Time out. Command cancelled')
        
        await ctx.message.channel.send(f'Thank you. I have got: "{ctx.message}" at {date_time}')
        
        
            
            
    @commands.command()
    async def delay_message(self, ctx, *, message: str):
        ctx.reply('Unused')
        if self.delayed_message.is_running():
            self.delayed_message.restart()
        else:
            self.delayed_message.start()
            
        
            
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
