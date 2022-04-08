from discord.ext import commands
import discord
import os
import json
import sys

# Cores: \033[{cor}m 'texto' \033[m
# Error         = 31: Vermelho      0xbb0000
# Correto       = 32: Verde         0x00bb00
# Alerta        = 33: Amarelo       0xbbbb00
# Processamento = 36: Cyan
# Usuario       = 90: Cinza Escuro

#https://convertingcolors.com


def load_inicial(bot): # Carrega todos os arquivos que estão nas pastas.
    for file in os.listdir("./Extensions"):
        try:
            if file.endswith(".py"):
                bot.load_extension(f"Extensions.{file[:-3]}")
                print(f"\033[32m|\033[m Modulo {file:^20} :\033[32mV\033[m:")
        except Exception as e:
            print(f"\033[31m|\033[m Modulo {file:^20} :\033[31mX\033[m:\n\033[31mError:\033[m {e}\n")
    print()
#---^




def config_get():
    try:
        with open('Extensions/config.json') as f:
            config = json.load(f)
            return config
    except:
        _token = input('TOKEN: ')
        _prefix = input('PREFIX: ')
        data = {"TOKEN": _token, "PREFIX": _prefix,}
        with open('Extensions/config.json', 'w') as f:
            f.write(json.dumps(data, indent=4))
        os.execv(sys.executable, ['python'] + sys.argv)

# Main:
os.system('mode 70,30');os.system('cls')
config = config_get()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=config['PREFIX'], case_insensitive = True, intents=intents)
bot.remove_command('help')

load_inicial(bot)


@bot.event
async def on_ready():
    print(f'\033[32m> \033[90m{bot.user}\033[m - \033[92mOnline\033[m')
    #print(f"\033[32m>\033[92m Online\033[m - \033[90m{bot.user}\033[m")


@bot.command(name='reload')
async def reload_cog(ctx, *, cog: str):
    cog = f"Extensions.{cog.capitalize()}"
    await ctx.send(f"Preparando para recarregar {cog}...", delete_after=5)
    bot.unload_extension(cog)
    try:
        bot.load_extension(cog)
        await ctx.send(f"{cog} cog foi recarregada com sucesso!", delete_after=5)
        print(f"{ctx.author} Recarregou: {cog}")
    except Exception as e:
        await ctx.send(f"```py\nError loading {cog}:\n\n{e}\n```", delete_after=5)

@bot.command(name= 'load')
async def load_cog(ctx, *, cog: str):
    cog = f"Extensions.{cog.capitalize()}"
    await ctx.send(f"Preparando para carregar {cog}...", delete_after=5)
    try:
        bot.load_extension(cog)
        await ctx.send(f"{cog} cog foi recarregada com sucesso!", delete_after=5)
        print(f"{ctx.author} Carregou: {cog}")
    except Exception as e:
        await ctx.send(f"```py\nError loading {cog}:\n\n{e}\n```", delete_after=5)


bot.run(config['TOKEN'])