import random
from discord.ext import commands

# Custom module import
from log import log_command


class clips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.message.reply('Oo. Ee. Ahh. BOIS')

    @commands.command()
    async def bois(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.bot.logger, 'bois')
        await ctx.message.reply(self.bot.config['bois']['url'])

    @commands.command()
    async def scuse(self, ctx):
        """Respond with a link to SydneyMGames clip"""
        log_command(ctx, self.bot.logger, 'scuse')
        await ctx.message.reply(self.bot.config['scuse']['url'])

    @commands.command()
    async def dolphin(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'dolphin')
        await ctx.message.reply(self.bot.config['dolphin']['url'])

    @commands.command()
    async def brenky(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'brenky')
        await ctx.message.reply(self.bot.config['brenky']['url'])

    @commands.command()
    async def batman(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'batman')
        await ctx.message.reply(self.bot.config['batman']['url'])

    @commands.command()
    async def soap(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'soap')
        await ctx.message.reply(self.bot.config['soap']['url'])

    @commands.command()
    async def blow(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'blow')
        await ctx.message.reply(self.bot.config['blow']['url'])

    @commands.command()
    async def bwah(self, ctx):
        """Respond with a link to BirdyRage clip"""
        log_command(ctx, self.bot.logger, 'bwah')
        await ctx.message.reply(self.bot.config['bwah']['url'])

    @commands.command()
    async def random_clip(self, ctx):
        """Respond with a random clip"""
        log_command(ctx, self.bot.logger, 'random_clip')

        clips = ('bois', 'scuse', 'brenky', 'dolphin', 'batman',
                 'soap', 'blow', 'bwah')

        clip = clips[random.randint(0, len(clips)-1)]
        await ctx.message.reply(self.bot.config[clip]['url'])

    @commands.command()
    async def clips(self, ctx):
        """Send a list of clip commands"""
        log_command(ctx, self.bot.logger, 'clips')

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


def setup(bot):
    bot.add_cog(clips(bot))
