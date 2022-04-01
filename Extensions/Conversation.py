from discord.ext import commands

bad_words = ['porra', 'caralho', 'buceta', 'inferno']

class Conversation(commands.Cog):
    def __init__(self, bot_pass):
        self.bot = bot_pass

    def comp(self, messagem:tuple, words:list):
        for i in messagem:
            if i in words:
                return True
        return False


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for item in bad_words:
            if item in message.content.lower():
                await message.channel.send(f'Por favor, {message.author}, não diga palavras feias!')
                await message.delete()

        if "kyoko" in message.content.lower():
            mensagem = message.content.lower().split(" ")
            
            if self.comp(mensagem, ["ola", "olá", "oi"]):
                await message.channel.send(f'Olá, {message.author.name}! :heart:')
            elif self.comp(mensagem, ["obrigado"]):
                await message.channel.send(f"Eu quem agradeço {message.author.name}")
            elif self.comp(mensagem, ["obr"]):
                await message.channel.send(f"Que nada Zé tamo aí.")
            elif self.comp(mensagem, ["opa"]):
                await message.channel.send(f'Opa {message.author.name}! :v:')
            elif self.comp(mensagem, ["tchau", "bye", "by"]):
                await message.channel.send(f'Bye Bye {message.author.name}! :wave: ')

def setup(bot_pass):
    bot_pass.add_cog(Conversation(bot_pass))