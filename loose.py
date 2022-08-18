import os
import random
import discord
from discord.ext import commands

# Custom module import
from log import log_command


class loose(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def good_bot(self, ctx):
        log_command(ctx, self.bot.logger, 'good_bot')
        for emoji in ('❤️', '💙', '💚', '🧡', '💜', '🤍', '💛', '🖤', '🤎'):
            await ctx.message.add_reaction(emoji)

    @commands.command()
    async def bad_bot(self, ctx):
        log_command(ctx, self.bot.logger, 'bad_bot')
        await ctx.message.add_reaction('👿')

    @commands.command()
    async def ciri(self, ctx):


        # Get a random .png from Ciri folder
        images = os.listdir(os.path.join(os.path.dirname(__file__), 'ciri'))
        images = [file for file in images if file.endswith('.png')]

        random_image = images[random.randint(0, len(images)-1)]
        random_image_path = os.path.join(os.path.dirname(__file__), 'ciri', random_image)

        file = discord.File(random_image_path, 'ciri.png')
        embed = discord.Embed(author='Smol',
                            title='Ciri',
                            description='Have a free ciri photo!')
        embed.set_image(url="attachment://ciri.png")
        await ctx.message.reply(file=file, embed=embed)

    @commands.command()
    async def cool(self, ctx):
        log_command(ctx, self.bot.logger, 'cool')

        if str(ctx.author)[:-5] == 'Smol_Tygr':
            await ctx.send('Smol is the coolest. No need to even check')
            return None

        coolness = random.randint(0, 101)
        message = "Function has broken. Balls."

        if coolness < 10:
            message = "Oh... Maybe don't let people know this"
        elif coolness < 30:
            message = "That's not very cool"
        elif coolness < 50:
            message = "Please try again, but harder"
        elif coolness < 70:
            message = "That's not bad!"
        elif coolness < 90:
            message = "Pretty damn cool!"
        elif coolness < 101:
            message = "So cool!"
        elif coolness == 101:
            message = "THE COOLEST."

        await ctx.send(f'{str(ctx.author)[:-5]} is {coolness}% cool. {message}')
        
        
async def setup(bot):
    await bot.add_cog(loose(bot))
