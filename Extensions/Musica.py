from discord.ext import commands
from youtube_dl import YoutubeDL
from random import randint
import discord




class Musica(commands.Cog):
  # Função inicial que declara as variaveis globais.
    def __init__(self, bot_pass) -> None:
        self.bot = bot_pass

        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS    = {"format": "bestaudio", "noplaylist":"True"}
        
        self.music_queue = []
        self.playing = []
        self.is_playing = False
        self.bot_voice_channel = None

  #-----^

    # Função loop que toca as muiscas da fila.
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            music_URL = self.music_queue[0]["source"]
            self.playing = self.music_queue[0]
            self.music_queue.pop(0)
            self.bot_voice_channel.play(discord.FFmpegPCMAudio(music_URL, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    


 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            self.play_next()
        else:
            self.is_playing = False
  #---------^


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as yt_dwl:
            try:
                
                print(f"\n\033[36m|\033[m Pesquisando por: \033[36m{item}\033[m.\033[36m")
                info = yt_dwl.extract_info("ytsearch:%s" % item, download=False)["entries"][0]
                print(f"\033[32m|\033[m Encontrado \033[36m{info['title']}\033[m.\n")
            except Exception:
                return False
        return info

  # Comando inicial para tocar musica.
    @commands.command(name="Tocar", aliases=["p", "play"], help="| 'p'   'play' | Reproduz uma música selecionada do youtube.")
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel # Nome do canal de voz
        except:
            words = [":x: Entre em um canal de voz.", ":x: Você não está em um canal de voz."]
            await ctx.channel.send(words[randint(0, (len(words)-1))])
            print(f"\033[33m|\033[m {ctx.author} tentou iniciar uma musica, mas não estava em um canal de voz.")
            return
        else:
            botMessage = await ctx.send(f" :mag_right: Pesquisando.")
            query_pass = self.search_yt(query)
            await botMessage.delete()

            if query_pass == False:
                
                words = ["É oque? não consegui entender !", "Escreva direito, seu burro !"]

                embedvc = discord.Embed(
                    title = f"| Erro ao carregar item !",
                    colour = 0xbb0000, # Vermelho
                    decription = f"Não foi possivel carregar o item.\n:{query}:"
                )
                await ctx.channel.send(words[randint(0, (len(words)-1))])
                await ctx.send(embed=embedvc)
                print(f"\033[31m|\033[m Erro ao carregar item: {args[0]}\n {query}")
            else:
                info_music = {
                    "source":       query_pass["formats"][3]["url"],
                    "title":        query_pass["title"],
                    "thumbnail":    query_pass["thumbnail"],
                    "upload_date":  query_pass["upload_date"],
                    "duration":     query_pass["duration"],
                    "view_count":   query_pass["view_count"],
                    "like_count":   query_pass["like_count"],
                    "webpage_url":  query_pass["webpage_url"],
                    "yt_channel":   query_pass["channel"],
                    "vc_channel":   voice_channel,
                    "author":       ctx.author.name
                }
                
                if len(self.music_queue) != 0 or self.is_playing == True:    
                    embedvc = discord.Embed(
                        title = f"| Musica adicionada à fila :",
                        colour = 0x00bb00, # Verde
                        description = f"{ctx.author.name} adicionou :\n[{info_music['title']}]({info_music['webpage_url']})"
                    )
                    embedvc.set_footer(text = f"Na posição #{len(self.music_queue)+1}")
                    embedvc.set_thumbnail(url = info_music["thumbnail"])
                    await ctx.send(embed=embedvc)
                    print(f"\033[32m|\033[90m {ctx.author}\033[m adicionou a música \033[36m{info_music['title']}\033[m à fila!")
                self.music_queue.append(info_music)
                if self.is_playing == False:
                  # reproduz a musica inicial
                    if len(self.music_queue) > 0:
                        if self.bot_voice_channel == None:
                            self.bot_voice_channel = await self.music_queue[0]["vc_channel"].connect()
                            if self.bot_voice_channel == None:
                                words = []

                                embedvc = discord.Embed(
                                    title = f"| Erro !",
                                    colour = 0xbb0000, # Vermelho
                                    description = f"Ouve um erro ao conectar ao canal de voz.\nUtilize '/sair' para reiniciar o bot."
                                )


                                print("Não foi possível conectar ao canal de voz.")
                        else:
                            await self.bot_voice_channel.move_to(self.music_queue[0]["vc_channel"])
                        await self.play_music(ctx)
                        embedvc = discord.Embed(
                            title = "| Tocando agora",
                            colour = 0x00bb00, # Verde
                            description = f""
                        ) #------------------------------------------------- AQUI

                    else:
                        self.is_playing = False
                        await self.bot_voice_channel.disconnect()
                  #-----^
  #---------------^

  # Comando para pausar e resumir
    @commands.command(name="Pause_resume", aliases=["pr", "para", "pausar", "resumir"], help="| 'pr'   'parar'   'pausar'   'resumir' | Pausa a música atual que está sendo reproduzida, ou retoma quando a musica esta parada.")
    async def pause_resume(self, ctx):
        if self.is_playing:
            self.bot_voice_channel.pause()
            self.is_playing = False

            # Criar embed

            print(f"\033[32m|\033[90m {ctx.author}\033[m pausou a musica!")
        else:
            self.bot_voice_channel.resume()
            self.is_playing = True

            # Criar embed

            print(f"\033[32m|\033[90m {ctx.author}\033[m retomou a musica!")
  #---------^

  # Comando para pular a musica
    @commands.command(name="Proxima", aliases=["sk", "skip", "next"], help="| 'sk'   'skip'   'next'   'proxima' | Passa para a proxima musica da fila.")
    async def skip(self, ctx):
        if self.bot_voice_channel != None:
            self.bot_voice_channel.stop()
            await self.play_music_loop(ctx)

            #criar Embed

            print(f"\033[32m|\033[90m {ctx.author}\033[m pulou a musica!")
        else:
            print('Sem musica tocando.')

            #criar Embed

  #---------^

  # Comando para mostrar os itens da fila.
    @commands.command(name="Fila", aliases=["f", "lista"], help="| 'f'   'lista' |\nExibe as músicas atuais na fila.")
    async def queue(self, ctx):
        row = ''
        queue = []
        for cont in range(0, len(self.music_queue)):
            row += f" {cont + 1} - **{self.music_queue[cont]['title']}**"
            queue.append(self.music_queue[cont]['title'])
        if len(queue) > 0:
            embedvc = discord.Embed(
                title = "| Tocando :",
                colour = 0x00bb00, # Verde
                description = f"[{self.playing[0]['title']}]({self.playing[0]['webpage_url']})\n`{self.playing[0]['duration']}`"
            )
            embedvc.set_thumbnail(url=self.playing[0]["thumbnail"])
            embedvc.set_footer(text=f"Pedido por {self.playing[0]['author']}")
            await ctx.send(embed=embedvc)
            embedvc = discord.Embed(
                title = (f"| Fila :"),
                colour = 0x00bb00, # Verde
                description = row
            )
            await ctx.send(embed=embedvc)
            print(f"\033[32m|\033[m Fila :")
            for i in range(len(queue)):
                print(f"\t{i+1} - \033[36m{queue[i]}\033[m")
        else:
            await ctx.send(f"A fila esta vazia.")
            

            print("Não existe musica na fila no momento.")
        print('')
  #-----^

  # Comando para limpar a fila
    @commands.command(name="Remover", aliases=["r", "remove"], help="| 'r'   'remove' |\nRemove todas as musicas da fila, ou apenas as que foram especificadas.")
    async def remove(self, ctx, *arg):
        if arg == ():
            self.music_queue = []
        else:
            item_args = []
            for item in arg:
                if item.isnumeric():
                    item = int(item)
                    item_args.append(item)
                else:
                    embedvc = discord.Embed(
                        title = f"| Atenção !",
                        colour= 0xbbbb00, # Amarelo
                        description = f"'**{item}**' não é um indice.\nTente usar o numero da fila."
                    )
                    await ctx.send(embed=embedvc)
                    print(f"\033[31m|\033[m \033[90m{ctx.author}\033[m: Tentou remover \033[31m{item}\033[m, mas não é um Indice.")
                    return
            item_args.sort(reverse=True)
            for item in item_args:
                if item > 0 and item <= len(self.music_queue):
                   pass
                else:                    
                    embedvc = discord.Embed(
                        title = "| Atenção !",
                        colour= 0xbbbb00, # Amarelo
                        description = f"A fila só vai até o item {len(self.music_queue)}"
                    )
                    await ctx.send(embed=embedvc)
                    print(f"\033[31m|\033[m \033[90m{ctx.author}\033[m: Tentou remover \033[31m{item}\033[m, mas não há musica.")
                    return
        
            desc = ""
            print(f"\033[32m|\033[m Removido :")
            for item in item_args:
                print(f"\t{item} - \033[31m{self.music_queue[item-1]['title']}\033[m")
                desc = f"{desc}\n{item} - **{self.music_queue[item-1]['title']}**"
                self.music_queue.pop(item-1)

            embedvc = discord.Embed(
                title = "| Itens removidos :",
                colour = 0x00bb00, # Verde
                description = desc
            )
            await ctx.send(embed=embedvc)
            await self.queue(ctx)

  #---------^

  # Comando para desconectar o bot no canal de voz
    @commands.command(name="Sair", aliases=["s", "leave"], help="| 's'   'leave' |\nDesconeta o bot do chat de voz.")
    async def disconnect(self, ctx):
        self.is_playing = False
        await self.bot_voice_channel.disconnect()
        print("Bot Desconectado do canal de voz.")
  #-----^

def setup(bot_pass):
    bot_pass.add_cog(Musica(bot_pass))