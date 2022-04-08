from discord.ext import commands
import discord


class Smarts(commands.Cog):
    def __init__(self, bot_pass):
        self.bot = bot_pass

    @commands.command(name="calcular", aliases=["calc"], help="| 'calc' | Calcula uma espreção basica.")
    async def calculate_args(self, ctx, *args):
        args = ''.join(args)
        response = eval(args)
        await ctx.send(f'A resposta é: {str(response)} seu burro!')


    @commands.command()
    async def ping(self, ctx):
        try:
            await ctx.send(f'Pong: {self.bot.ws.latency * 1000:.0f} ms')
        except discord.HTTPException:
            print("Erro: Ping")

def setup(bot_pass):
    bot_pass.add_cog(Smarts(bot_pass))