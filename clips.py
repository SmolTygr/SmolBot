import random
import logging
import discord
from discord.ext import commands

# Custom module import
from log import log_command


class Clips(commands.Cog):
    def __init__(self, bot, logger: logging.Logger, config: dict):
        self.bot = bot
        self.logger = logger
        self.config = config

    # @commands.command()
    # async def test(self, ctx):
    #     await ctx.message.reply('fuck off')


    @commands.command()
    async def bois(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.logger, 'bois')
        await ctx.message.reply(self.config['bois']['url'])

    @commands.command()
    async def scuse(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.logger, 'scuse')
        await ctx.message.reply(self.config['scuse']['url'])

    @commands.command()
    async def dolphin(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'dolphin')
        await ctx.message.reply(self.config['dolphin']['url'])

    @commands.command()
    async def brenky(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'brenky')
        await ctx.message.reply(self.config['brenky']['url'])

    @commands.command()
    async def batman(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'batman')
        await ctx.message.reply(self.config['batman']['url'])

    @commands.command()
    async def soap(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'soap')
        await ctx.message.reply(self.config['soap']['url'])

    @commands.command()
    async def blow(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'blow')
        await ctx.message.reply(self.config['blow']['url'])

    @commands.command()
    async def bwah(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'bwah')
        await ctx.message.reply(self.config['bwah']['url'])

    @commands.command()
    async def random_clip(self, ctx):
        """Respond with a random clip"""
        log_command(ctx, self.logger, 'random_clip')

        clips = ('bois', 'scuse', 'brenky', 'dolphin', 'batman',
                 'soap', 'blow', 'bwah')

        clip = clips[random.randint(0, len(clips)-1)]
        await ctx.message.reply(self.config[clip]['url'])

    @commands.command()
    async def clips(self, ctx):
        """Send a list of clip commands"""
        log_command(ctx, self.logger, 'clips')

        message = """Some amazing clips from the best streamers:
            !bois
            !scuse
            !brenky
            !dolphin
            !batman
            !soap
            !blow
            !bwah
            
        If you want a random one:
            !random_clip
        """
        await ctx.message.reply(message)
