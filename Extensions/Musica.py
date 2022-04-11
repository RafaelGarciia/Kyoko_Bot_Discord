from discord.ext    import commands
from youtube_dl     import YoutubeDL
from random         import randint
import discord

class Musica(commands.Cog):
  # Função inicial que declara as variaveis globais.
    def __init__(self, bot_pass) -> None:
        self.bot = bot_pass

        self.FFMPEG_OPTIONS     = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS        = {"format": "bestaudio", "noplaylist":True} #{"format": "139", "noplaylist": True, "outtmpl": 'music', "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": 'mp3', "preferredquality": '128'}]}
        self.music_queue        = []
        self.is_playing         = {'playing': False, 'title': None, 'thumbnail': None, 'webpage_url': None, 'author': None}
        self.bot_voice_channel  = None
  #-----^

    async def check_queue(self, ctx):
        if len(self.music_queue) > 0:
            ctx.voice_client.stop()
            await self.play_music_loop(ctx)


  # Função loop que toca as muiscas da fila.
    async def play_music_loop(self, ctx):
        if len(self.music_queue) > 0:
            self.bot_voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.music_queue[0]["source"], **self.FFMPEG_OPTIONS)), after=lambda e: ctx.bot.loop.create_task(self.check_queue(ctx)))
            self.is_playing.update({'playing': True, 'title': self.music_queue[0]["title"], 'thumbnail': self.music_queue[0]["thumbnail"], 'webpage_url': self.music_queue[0]['webpage_url'], 'author_name': self.music_queue[0]['author_name'], 'author_id': self.music_queue[0]['author_id']})
            self.music_queue.pop(0)

            embedvc = discord.Embed(
                title = "| Tocando :",
                colour = 0x00bb00, # Verde
                description = f"[{self.is_playing['title']}]({self.is_playing['webpage_url']})"
            )
            embedvc.set_thumbnail(url=self.is_playing["thumbnail"])
            embedvc.set_footer(text=f": Pedido por {self.is_playing['author_name']} :")
            await ctx.send(embed=embedvc)
            print(f"\033[32m>\033[m Tocando agora:\n\033[32m|\033[m  \033[36m{self.is_playing['title']}\033[m : \033[90m{self.is_playing['author_name']}\033[m")
        else:
            self.is_playing['playing'] = False
  #---------^


  # Comando inicial para tocar musica.
    @commands.command(name="Tocar", aliases=["p", "play"], help="| 'p'   'play' | Reproduz uma música selecionada do youtube.")
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel # Nome do canal de voz
        except:
            embedvc = discord.Embed(
                title = "| Atenção !",
                colour = 0xbbbb00, # Amarelo
                description = f"Você não está em um canal de voz."
            )
            await ctx.send(embed=embedvc)
            print(f"\033[33m|\033[m {ctx.author} tentou iniciar uma musica, mas não estava em um canal de voz.")
            return # Finaliza a Função.
        else:
          # Pesquisa a musica no youtube:
            with YoutubeDL(self.YDL_OPTIONS) as yt_dwl:
                mens = []
                try:
                    mens.append(await ctx.send(':mag_right: Pesquisando...'))
                    print(f"\n\033[36m|\033[m Pesquisando por: \033[36m{query}\033[m.\033[36m")
                    info = yt_dwl.extract_info("ytsearch:%s" % query, download=False)["entries"][0]
                    # print(f"\033[32m|\033[m Encontrado \033[36m{info['title']}\033[m.")
                    print('\033[m')

                    info_music = {
                        "source":       info["formats"][3]["url"],
                        "title":        info["title"],
                        "thumbnail":    info["thumbnail"],
                        "upload_date":  info["upload_date"],
                        "duration":     f"0{(int(info['duration'])/60):.2f}".replace('.', ':'),
                        "view_count":   info["view_count"],
                        "like_count":   info["like_count"],
                        "webpage_url":  info["webpage_url"],
                        "yt_channel":   info["channel"],
                        "vc_channel":   voice_channel,
                        "author_name":  ctx.author.name,
                        "author_id":    ctx.author.id
                    }

                except Exception:
                    mens.append(await ctx.send('Erro ao carregar'))
                    info_music = False     # Não conseguiu achar a musica
          #---------^
            for item in mens:
                await item.delete()
            if info_music == False:
                embedvc = discord.Embed(
                    title = f"| Erro ao carregar item !",
                    colour = 0xbb0000, # Vermelho
                    decription = f"Não foi possivel carregar o item.\n:{query}:"
                )
                await ctx.send(embed=embedvc)
                print(f"\033[31m|\033[m Erro ao carregar item:\n {query}")
            else:
                if len(self.music_queue) > 1 or self.is_playing['playing'] == True:
                    embedvc = discord.Embed(
                        title = f"| Musica adicionada á fila :",
                        colour = 0x00bb00, # Verde
                        description = f"\n[{info_music['title']}]({info_music['webpage_url']})\n"
                    )
                    embedvc.set_thumbnail(url=info_music["thumbnail"])
                    embedvc.set_footer(text=f": Adicionado por {info_music['author_name']} :")
                    await ctx.send(embed=embedvc)
                    print(f"\033[32m|\033[90m {ctx.author}\033[m adicionou a música \033[36m{info_music['title']}\033[m à fila!")
                self.music_queue.append(info_music)
                if self.is_playing['playing'] == False:
                  # reproduz a musica inicial
                    if len(self.music_queue) > 0:
                        if self.bot_voice_channel == None:
                            self.bot_voice_channel = await self.music_queue[0]["vc_channel"].connect()
                            if self.bot_voice_channel == None:

                                embedvc = discord.Embed(
                                    title = f"| Erro !",
                                    colour = 0xbb0000, # Vermelho
                                    description = f"Ouve um erro ao conectar ao canal de voz.\nUtilize '/sair' para reiniciar o bot."
                                )

                                print("Não foi possível conectar ao canal de voz.")
                        else:
                            await self.bot_voice_channel.move_to(self.music_queue[0]["vc_channel"])
                        await self.play_music_loop(ctx)
                        #print('Tocar musica, é para ja')
                    else:
                        self.is_playing['playing'] = False
                        await self.bot_voice_channel.disconnect()
                  #-----^
  #---------------^

    # Comando para pausar e resumir
    @commands.command(name="Pause_resume", aliases=["pause", "pausar"], help="| 'pr'   'parar'   'pausar'   'resumir' | Pausa a música atual que está sendo reproduzida, ou retoma quando a musica esta parada.")
    async def pause_resume(self, ctx):
        if self.is_playing['playing']:
            self.bot_voice_channel.pause()
            self.is_playing['playing'] = False

            # Criar embed

            print(f"\033[32m|\033[90m {ctx.author}\033[m pausou a musica!")
        else:
            self.bot_voice_channel.resume()
            self.is_playing['playing'] = True

            # Criar embed

            print(f"\033[32m|\033[90m {ctx.author}\033[m retomou a musica!")
  #---------^

    @commands.command(name="Resume", aliases=["Resumir"], help="| 'resume' 'resumir' | Da play em uma musica parada.")
    async def resume(self, ctx):
        if self.is_playing['playing']:
            ctx.send(f"Musica já esta tocando.")
        else:
            self.bot_voice_channel.resume()
            self.is_playing['playing'] = True
            print(f"\033[32m|\033[90m {ctx.author}\033[m retomou a musica!")
  
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
        item_queue = []
        w = f"**Tocando agora:** [{self.is_playing['title']}]({self.is_playing['webpage_url']})\n"
        for i in range(0, len(self.music_queue)):
            w = f"{w}\n **{i+1} -** [{self.music_queue[i]['title'][:55]}]({self.music_queue[i]['webpage_url']})"
            item_queue.append(f'{self.music_queue[i]["title"]}')
        if len(item_queue) > 0:

            embedvc = discord.Embed(
                title = (f"| Fila :"),
                colour = 0x00bb00, # Verde
                description = w
            )
            await ctx.send(embed=embedvc)
            print(f"\033[32m|\033[m Fila :")
            for i in range(len(item_queue)):
                print(f"\t{i+1} - \033[36m{item_queue[i]}\033[m")
        else:
            
            # Criar Embed

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
                self.music_queue.pop(item)

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
        self.is_playing['playing'] = False
        await self.bot_voice_channel.disconnect()
        print("Bot Desconectado do canal de voz.")
  #-----^



def setup(bot_pass):
    bot_pass.add_cog(Musica(bot_pass))