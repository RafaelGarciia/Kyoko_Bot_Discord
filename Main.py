import discord
from discord.ext import commands
import os 
import BOT_Token

# Cores: \033[{cor}m 'texto' \033[m
# Error         = 31: Vermelho
# Correto       = 32: Verde
# Alerta        = 33: Amarelo
# Processamento = 36: Cyan
# Usuario       = 90: Cinza Escuro


def load_cogs(bot): # Carrega todos os arquivos que estão nas pastas.
    #bot.load_extension("manager")
    for file in os.listdir("./Extensions"):
        if file.endswith(".py"):
            print(f"\033[32m|\033[m Modulo '{file}' carregado.")
            bot.load_extension(f"Extensions.{file[:-3]}")
    print('\033[32m|\033[m Arquivos carregados...')
#-----------^

# Main:
#os.system('mode 70,30');os.system('cls')
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