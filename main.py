import discord
import os
import struct
import requests
import json
import asyncio
import pytz
import pickle
from replit import db
from datetime import datetime, timezone

client = discord.Client()

# Notas de continuação de trabalho ------------------------------------------------------
# implementar perfil_titulo
# faltando aumentar/reduzir o contador de membros de cada ocupacao

# Area para testes idiotas --------------------------------------------------------------
#print(db.keys())

# Variaveis Inicializadas ---------------------------------------------------------------

#Configuracao do horario

set(pytz.all_timezones_set)
tz = pytz.timezone('America/Cuiaba')

# Objetos -------------------------------------------------------------------------------
class Recursos:
  # self, int, int, int, int
  def __init__(self, ouro, prestigio, devocao, renome):
    self.ouro = ouro
    self.prestigio = prestigio
    self.devocao = devocao
    self.renome = renome
class Ocupacao:
  # self, int, class(), int
  def __init__(self, tier, recursos, numero_de_membros):
    self.tier = tier
    self.recursos = recursos
    self.membros = numero_de_membros
class Familia:
  # self, string, int, string(id), array[id(string)]
  def __init__(self, nome, renome, chefe, membros):
    self.nome = nome
    self.renome = renome
    self.chefe = chefe
    self.membros = membros
class Titulo:
  # self, string, string, int, id(string), id(string)
  def __init__(self, nome_do_titulo, nome_da_terra, tier, dono, vassalo):
    self.nome = nome_do_titulo
    self.terra = nome_da_terra
    self.tier = tier
    self.dono = dono
    self.vassalo = vassalo
class Usuario:
  # self, string, string, recursos(), string, string, array[titulo()]
  def __init__(self, id, nome, recursos, id_ocupacao, id_familia, titulo):
    self.id = id
    self.nome = nome
    self.recursos = recursos
    self.ocupacao = id_ocupacao
    self.familia = id_familia
    self.titulo = titulo

#Listas --------------------------------------------------------------------------------
    
# Variáveis sistêmicas armazenadas no bd
# Horas
# db['sistema'] = [0]
# db['ocupacoes'] = {}
# db['familias'] = {}
# db['titulos'] = {}

# Dicionario de Ocupacoes
# Nome, Tier, Recursos()
# Recursos()
# Ouro, Prestigio, Devocao, Renome
    
#DOcupacoes = {
#  'Desocupado':  Ocupacao(0, Recursos(1, 1, 1, -1), 0),
#  'Fazendeiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Cozinheiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Lenhador':    Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Marceneiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Minerador':   Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Ferreiro':    Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Ladrao':      Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Mercenario':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
#  'Herbalista':  Ocupacao(0, Recursos(3, 1, 5, 0), 0)
#}

#Dicionario de Familias
#DFamilias = {}

#Dicionario de Titulos
#DTitulos = {
#  'Campones':  Titulo('Campones', 'Capital', 0, 'null','null'),
#  'Barao':     Titulo('Barao', '', 1, '', ''),
#  'Nobre':     Titulo('Nobre', '', 2, '', ''),
#  'Moeda':     Titulo('Mestre da moeda', '', 5, '', ''),
#  'Marechal':  Titulo('Marechal', '', 5, '', ''),
#  'Espiao':    Titulo('Mestre da espionagem', '', 5, '', ''),
#  'Capelao':   Titulo('Capelao', '', 5, '', ''),
#  'Chanceler': Titulo('Chanceler', '', 6, '', ''),
#  'Conde':     Titulo('Conde', '', 7, '', ''),
#  'Duque':     Titulo('Duque', '', 8, '', ''),
#  'Rei':       Titulo('Rei', '', 9, '', ''),
#  'Imperador': Titulo('Imperador', '', 10, '', 'null')
#}

@client.event
async def on_ready():
  # Evento - Ao iniciar
  print("{0.user} está online.\nDeixe os reinos cairem...".format(client))
  await controlador_de_tempo()

@client.event
async def on_member_join(member):
  # Evento - Quando alguém entra no servidor
  if (db[str(member.id)] == member.id):
    print('Seja bem vindo de volta, '+{member.nick}+'.')
    return

  else:
    await message.channel.send('Seja bem vindo, '+{member.nick}+'.\n' + \
    'Digite **vsf** em #comandos para mais informacoes.')
  await controlador_de_tempo()



@client.event
async def on_message(message):
  # Evento - Ao chamar o bot
  if (message.author == client.user):
    # Se a mensagem for do proprio bot, nao faz nada
    return
  mensagem = message.content.split(' ',)
  mensagem += '?'
  if mensagem[0] == 'vsf':
    # Menu Principal
    if mensagem[1] in ['1', 'perfil', 'p']:
      #1 Meu perfil
      await perfil_handler(str(message.author.id), mensagem, message)
    #elif mensagem[1] in ['2', 'lugares', 'l']:
      #2 Lugares
      #return
        #2.1 Lugares - Onde estou
          #2.1.1 Lugares - Onde estou - Cidade (1/3)
          #2.1.2 Lugares - Onde estou - Igreja (0/3)
          #2.1.3 Lugares - Onde estou - Baronato (0/3)
          #2.1.4 Lugares - Onde estou - Capital (0/5)
        #2.2 Lugares - Terras (0/12)
          #2.2.0 Lugares - Terras - 0 Capital
          #2.2.X Lugares - Terras - 1-12 (Vazio)
        #2.3 Lugares - 

    elif mensagem[1] in ['80', 'ocupacoes', 'o']:
      #80 Ocupacoes - Edicao e criacao de ocupacoes
      await ocupacoes_handler(str(message.author.id), mensagem, message)
      
    elif mensagem[1] in ['96', 'meudb']:
      #96 Teste - Printa seu próprio db
      print(db[str(message.author.id)])
      author = load(str(message.author.id))
      print(author)
    
    elif mensagem[1] in ['97', 'sistema']:
      #97 Teste - Printa as informacoes de sistema
      print (db['sistema'])
      
    elif mensagem[1] in ['98','console']:
      #98 Teste - Printa a lista de ocupacoes no console
      DOcupacoes = load('ocupacoes')
      print (DOcupacoes)

    elif mensagem[1] in ['0','00','conta','c']:
      #0 Conta
      await conta_handler(str(message.author.id), mensagem, message)

    #? Ajuda
    else:
      await message.channel.send('```Precisa de ajuda?\n' + \
      '1. perfil/p - Exibe as informacoes do seu personagem.\n'+ \
      '80. ocupacoes/o - [Adm] Edicao e criacao de ocupacoes\n' + \
      '96. meudb - Printa seu proprio db no console.\n' + \
      '97. sistema - Printa as informacoes de sistema.\n' + \
      '98. console - Printa a lista de ocupacoes no console.\n'+ \
      '00. conta/c - Cadastro e opcoes de conta.' + \
      '```')

  await controlador_de_tempo()

# Funções assincronas ------------------------------------------------------------------
async def evita_spam():
  # Evita spam: NotOk
  intervalo_de_tempo = int(time.time())
  
async def controlador_de_tempo():
  # Loop para atualizar os recursos dos jogadores a cada hora: Ok
  # Mas pode melhorar
  while True:
    horario = datetime.now(tz=tz)
    if db['sistema'][0] != horario.hour:
      if db['sistema'][0] < 23:
        proxima_hora = db['sistema'][0] + 1
      else:
        proxima_hora = 1
      db['sistema'][0] = horario.hour
      lucro_profissao()
    else:
      await asyncio.sleep(60)

async def perfil_handler(author_id, mensagem, message) -> None:
  author = load(author_id)
  #1 Meu perfil: Ok
  if mensagem[2] in ['1', 'recursos', 'r']:
    #1.1 Meu perfil - Recursos
    await perfil_recursos(author, message)
  elif mensagem[2] in ['2', 'ocupacao', 'o']:
    #1.2 Meu perfil - Mudar de ocupacao
    await perfil_ocupacao(author, mensagem)
  elif mensagem[2] in ['3', 'familia', 'f']:
    #1.3 Meu perfil - Minha familia
    await perfil_familia(author, mensagem, message)
  elif mensagem[2] in ['4', 'titulo', 't']:
    #1.4 Meu perfil - Meus titulos
    await perfil_titulo(author, mensagem, message)
  else:
    #1.? Meu perfil - Ajuda
    await message.channel.send('```Meu perfil\n'+ \
    '1. recursos/r - Mostra os recursos que voce possui.\n'+ \
    '2. ocupacao/o - Permite trocar de ocupacao.\n'+ \
    '3. familia/f - Ver informacoes da minha familia\n' + \
    '4. titulo/t - Escolha qual titulo associar ao seu nome\n' + \
    '```')

async def perfil_recursos(author, message) -> None:
  #1.1 Meu perfil - Recursos: Ok
  DOcupacoes = load('ocupacoes')
  await message.channel.send('```Meu perfil\n'+ \
    '\n\nOuro: ' + str(author.recursos.ouro)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.ouro)+')' + \
    '\nPrestigio: ' + str(author.recursos.prestigio)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.prestigio) + ')' + \
    '\nDevocao: ' + str(author.recursos.devocao)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.devocao)+ ')' + \
    '\nRenome: +(' + \
    str(DOcupacoes[author.ocupacao].recursos.renome)+ ')' + \
    '```')

async def perfil_ocupacao(author, mensagem) -> None:
  #1.2 Meu perfil - Ocupacao: Ok
  DOcupacoes = load('ocupacoes')
  if (mensagem[3] in DOcupacoes.keys()):
    #1.2.X Meu perfil - Mudar de ocupacao - Ocupacao escolhida: Ok
    author.ocupacao = DOcupacoes[mensagem[3]].nome
    db[author.id] = dump(author)
    await message.channel.send('```Sua ocupacao mudou.\n' + \
    'Agora voce e: ' + author.ocupacao + \
    '```')
  else:
    #1.2.? Meu perfil - Mudar de ocupacao - Ajuda: Ok
    await message.channel.send('```Lista de ocupacoes:```')
    await message.channel.send (DOcupacoes.keys())

async def perfil_familia(author, mensagem, message) -> None:
  #1.3 Meu perfil - Minha familia: Ok
  DFamilias= load('familias')
  if mensagem[3] in ['1', 'membros', 'm']:
    #1.3.1 Meu perfil - Minha familia - Membros
    await perfil_familia_membros(author, message, DFamilias)
      
  elif mensagem[3] in ['2', 'chefe', 'c']:
    #1.3.2 Meu Perfil - Minha familia - Chefe
    await perfil_familia_chefe(author, message, DFamilias)
  
  elif mensagem[3] in ['9', 'juntar', 'j']:
    #1.3.9 Meu perfil - Minha familia - Ser adotado
    await perfil_familia_juntar(author, mensagem, message, DFamilias)
    
  elif mensagem[3] in ['0','criar']:
    #1.3.0 Meu perfil - Minha familia - Criar uma familia
    await perfil_familia_criar(author, mensagem, message, DFamilias)      
    
  else:
    await message.channel.send('```Minha familia:\n' + \
    '1. membros/m - Mostra a lista de membros da sua familia\n' + \
    '2. chefe/c - Mostra quem e o chefe da sua familia\n' + \
    '9. juntar/j - Se juntar a uma familia ja existente\n' + \
    '0. criar - Cria uma nova familia (e abandonar a atual)\n' + \
    '```')

async def perfil_familia_membros(author, message, DFamilias) -> None:
  #1.3.1 Meu perfil - Minha familia - Membros: Ok
  if (author.familia == ''):
    return await message.channel.send("```Você ainda não pertence a nenhuma familia.\nJunte-se a uma das familias existentes ou crie a sua!```")
  else:
    if DFamilias[author.familia].membros:
      await message.channel.send(DFamilias[author.familia].membros)
    else:
      await message.channel.send('```Essa familia nao tem membros ainda.```')

async def perfil_familia_chefe(author, message, DFamilias) -> None:
  #1.3.2 Meu Perfil - Minha familia - Chefe: Ok
  if (author.familia == ''):
    return await message.channel.send("```Você ainda não pertence a nenhuma familia.\nJunte-se a uma das familias existentes ou crie a sua!```")
  else:
    if DFamilias[author.familia].chefe == author.id:
      await message.channel.send('Voce e o chefe de sua familia!')
    else:
      await message.channel.send('O chefe de sua familia é: ' + db[DFamilias[author.familia].chefe].nome)

async def perfil_familia_juntar(author, mensagem, message, DFamilias) -> None:
  #1.3.9 Meu perfil - Minha familia - Ser adotado
  if mensagem[4] in DFamilias:
    #Se já estiver em uma familia
    if not author.familia:
      if (DFamilias[author.familia].chefe == author.id):
        DFamilias[mensagem[4]].renome += int(DFamilias[author.familia].renome / 2)
        if(DFamilias[author.familia].membros):
          DFamilias[author.familia].chefe = DFamilias[author.familia].membros[0]
          pop(DFamilias[author.familia].membros[0])
          DFamilias[author.familia].renome = int(DFamilias[author.familia].renome/2)
          author.recursos.prestigio -= 300
          await message.channel.send('```Abandonar sua familia e considerado um ato desprezivel.\nPrestigio[-300]```')
        else:
          pop(DFamilias[author.familia])
          author.recursos.prestigio -= 100
          await message.channel.send('```Renegou seu sobrenome e desfez sua familia.\nPrestigio[-100]```')
      else:
        DFamilias[author.familia].membros.remove(author.id)
        author.recursos.prestigio -= 100
        await message.channel.send('```Renegou seu sobrenome.\nPrestigio[-100]```')
    author.familia = mensagem[4]
    DFamilias[author.familia].membros.append(author.id)
    db[author.id] = dump(author)
    db['familias'] = dump(DFamilias)
    await message.channel.send('```Juntou-se a familia com sucesso.```')      
  else:
    await message.channel.send('```Escolha uma familia existente:```')
    await message.channel.send(DFamilias.keys())

async def perfil_familia_criar(author, mensagem, message, DFamilias) -> None:
  if mensagem[4] in DFamilias.keys():
    await message.channel.send('```Esse nome de familia já existe.```')
  elif mensagem[4] in ['?']:
    await message.channel.send('```Escolha um sobrenome para a familia.```')
  else:
    DFamilias[mensagem[4]] = Familia(mensagem[4],0,author.id,[])
    author.familia = mensagem[4]
    db['familias'] = dump(DFamilias)
    db[author.id] = dump(author)
    await message.channel.send('```Familia criada com sucesso.```')

async def perfil_titulo(author, mensagem, message) -> None:
  #1.4 Meu perfil - Meus titulos
  return

async def ocupacoes_handler(author, mensagem, message) -> None:
  #80 Ocupacoes: Ok
  DOcupacoes = load('ocupacoes')
  if mensagem [2] in ['1', 'criar', 'c']:
    #80.1 Ocupacoes - Criar
    await ocupacoes_criar(mensagem, DOcupacoes)
  elif mensagem[2] in ['2', 'lista', 'l']:
    #80.2 Ocupacoes - Lista
    await ocupacoes_lista(message, DOcupacoes)
  elif mensagem[2] in ['3', 'apagar', 'a']:
    await ocupacoes_apagar(mensagem, message, DOcupacoes)
  else:
    #80.? Ocupacoes - Ajuda
    await message.channel.send('```Ocupacoes\n' + \
    '1. criar/c - Cria uma nova ocupacao\n' + \
    '2. lista/l - Mostra a lista de ocupacoes\n' + \
    '3. editar/e - Editar uma ocupacao existente\n' + \
    '0. apagar/a - Apaga uma ocupacao' + \
    '```')
    
async def ocupacoes_criar(mensagem, DOcupacoes) -> None:
  #80.1 Ocupacoes - Criar: Ok
  if mensagem[3] != '?' and mensagem[3] not in DOcupacoes.keys():
    nova_ocupacao = Ocupacao(int(mensagem[4]), Recursos(int(mensagem[5]), int(mensagem[6]), int(mensagem[7]), int(mensagem[8])), 0)
    DOcupacoes[mensagem[3]] = nova_ocupacao
    db['ocupacoes'] = dump(DOcupacoes)
    await message.channel.send("```Ocupacao criada com sucesso.```")
  else:
    await message.channel.send('```Ocupacao: Nome[string], Tier[int], Recursos[class()]```')

async def ocupacoes_lista(message, DOcupacoes) -> None:
  #80.2 Ocupacoes - Lista: Ok
  await message.channel.send(DOcupacoes.keys())

async def ocupacoes_apagar(mensagem, message, DOcupacoes) -> None:
  #80.0 Ocupacoes - Apagar: Ok
  if mensagem[3] in DOcupacoes.keys():
    DOcupacoes.pop(mensagem[3])
    db['ocupacoes'] = dump(DOcupacoes)
    await message.channel.send('```Ocupacao apagada com sucesso.```')
  else:
    await message.channel.send('```Ocupacao nao existe.```')
  
async def conta_handler(author_id, mensagem, message) -> None:
  #0 Gerencia opcoes da conta do usuario: Ok
  if mensagem[2] in ['1','cadastro','reset']:
    #0.1 Conta - Cadastro / Reset
    await conta_cadastro(author_id, message)
  elif mensagem[2] in ['0', 'apagar']:
    await conta_apagar(author_id, message)
    #0.0 Conta - Apagar conta
  else:
    #0.? Conta - Ajuda
    await message.channel.send('```Minha conta\n'+ \
    '1. cadastro/reset - Resets nao podem ser revertidos.\n' + \
    '0. apagar - Essa acao exclui a sua conta.' + \
    '```')
    
async def conta_cadastro(author_id, message):
  #0.1 Conta - Cadastro / Reset: Ok
  usuario = Usuario(author_id, message.author.name + message.author.discriminator, Recursos(0,0,0,0), 'Desocupado', '', ['Campones'])
  db[author_id] = dump(usuario)
  DOcupacoes = load('ocupacoes')
  DOcupacoes['Desocupado'].membros += 1
  db['ocupacoes'] = dump(DOcupacoes)
  await message.channel.send('```Conta criada/resetada com sucesso.```')

async def conta_apagar(author_id, message):
  #0.0 Conta - Apagar conta: Ok
  del db[str(author_id)]
  await message.channel.send('```Conta apagada com sucesso.```')


# Funcoes sincronas --------------------------------------------------------------------
def load(coisa):
  try:
    a = pickle.loads(db[coisa].encode('latin1'))
    print(db['coisa'], 'sucessinho aqui')
    return a
  except:
    print(coisa, db[coisa], type(db[coisa]))
def dump(coisa):
  return pickle.dumps(coisa).decode('latin1')
  
def lucro_profissao():
  # Gera recursos para os jogadores : Ok
  DFamilias = load('familias')
  DOcupacoes = load('ocupacoes')
  for user_id in db.keys():
    if user_id not in ['sistema', 'ocupacoes', 'familias', 'titulos']:
      usuario = load(user_id)
      usuario.recursos.ouro += DOcupacoes[usuario.ocupacao].recursos.ouro
      usuario.recursos.prestigio += DOcupacoes[usuario.ocupacao].recursos.prestigio
      usuario.recursos.devocao += DOcupacoes[usuario.ocupacao].recursos.devocao
      DFamilias[usuario.familia].renome = usuario.recursos.renome
      db[user_id] = dump(usuario)
  db['familias'] = dump(DFamilias)

client.run(os.environ['DATABASE_PASSWORD'])
# Senha do DB