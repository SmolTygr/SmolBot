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

    @commands.command()
    async def bois(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.logger, 'bois')
        await ctx.message.reply(self.config['bois']['url'])

    @commands.command(name='scuse')
    async def _(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.logger, 'scuse')
        embed = discord.Embed(**self.config['scuse'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='dolphin')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'dolphin')
        embed = discord.Embed(**self.config['dolphin'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='brenky')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'brenky')
        embed = discord.Embed(**self.config['brenky'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='batman')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'batman')
        embed = discord.Embed(**self.config['batman'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='soap')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'soap')
        embed = discord.Embed(**self.config['soap'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='blow')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'blow')
        embed = discord.Embed(**self.config['blow'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='bwah')
    async def _(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.logger, 'bwah')
        embed = discord.Embed(**self.config['bwah'])
        await ctx.message.reply(embed=embed)

    @commands.command(name='random_clip')
    async def _(self, ctx):
        """Respond with a random clip"""
        log_command(ctx, self.logger, 'random_clip')

        clips = ('bois', 'scuse', 'brenky', 'dolphin', 'batman',
                 'soap', 'blow', 'bwah')

        clip = clips[random.randint(0, len(clips)-1)]
        embed = discord.Embed(**self.config[clip])
        await ctx.message.reply(embed=embed)
