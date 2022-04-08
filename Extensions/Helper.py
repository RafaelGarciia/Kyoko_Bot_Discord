from shutil import register_unpack_format
import discord
from discord.ext import commands


class Helper(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command(name="Help",aliases=['h', 'ajuda'],help="| 'h'   'ajuda' |\nComando de ajuda\nArgs:\n[- ] Para listagem horizontal\n[+] Para listagem em grade.")
    async def help(self, ctx, *args):
        if len(args) == 0 or args[0] == '-':
            helptxt = ''
            for command in self.client.commands:
                helptxt += (f'**{command}** - {command.help}\n\n')
            embedhelp = discord.Embed(
                colour = 1646116,#grey
                title=f'Comandos para a {self.client.user.name}',
                description = helptxt+'\nA seu dispor ^^')
        elif args[0] == '+':
            comand_name = []
            comand_help = []
            for command in self.client.commands:
                comand_name.append(command.name)
                comand_help.append(command.help)
            embedhelp = discord.Embed(
                colour = 1646116,#grey
                title=f'Comandos para a {self.client.user.name}',
                description = 'A seu dispor ^^')
            for i in range(len(comand_name)):
                embedhelp.add_field(name=comand_name[i], value=comand_help[i], inline=True)
        else:
            print (f'Parametro invalido{args}.')
            return

        embedhelp.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embedhelp)


def setup(client):
    client.add_cog(Helper(client))