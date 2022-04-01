import discord
from discord.ext import commands
import os 
import BOT_Token

# Cores: \033[{cor}m 'texto' \033[m
# Error         = 31: Vermelho      0xbb0000
# Correto       = 32: Verde         0x00bb00
# Alerta        = 33: Amarelo       0xbbbb00
# Processamento = 36: Cyan
# Usuario       = 90: Cinza Escuro

#https://convertingcolors.com


def load_cogs(bot): # Carrega todos os arquivos que estão nas pastas.
    for file in os.listdir("./Extensions"):
        try:
            if file.endswith(".py"):
                bot.load_extension(f"Extensions.{file[:-3]}")
                print(f"\033[32m|\033[m Modulo {file:^20} :\033[32mV\033[m:")
        except Exception as e:
            print(f"\033[31m|\033[m Modulo {file:^20} :\033[31mX\033[m:\n\033[31mError:\033[m {e}\n")
    print()
#-----------^

# Main:
os.system('mode 70,30');os.system('cls')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', case_insensitive = True, intents=intents)
bot.remove_command('help')
load_cogs(bot)

@bot.event
async def on_ready():
    print(f'\033[32m> \033[90m{bot.user}\033[m - \033[92mOnline\033[m')
    #print(f"\033[32m>\033[92m Online\033[m - \033[90m{bot.user}\033[m")




bot.run(BOT_Token.TOKEN)