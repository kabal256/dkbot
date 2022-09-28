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
DOcupacoes = {
  'Desocupado':  Ocupacao(0, Recursos(1, 1, 1, -1), 0),
  'Fazendeiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Cozinheiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Lenhador':    Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Marceneiro':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Minerador':   Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Ferreiro':    Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Ladrao':      Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Mercenario':  Ocupacao(0, Recursos(3, 1, 5, 0), 0),
  'Herbalista':  Ocupacao(0, Recursos(3, 1, 5, 0), 0)
}

#Dicionario de Familias
DFamilias = {}

#Dicionario de Titulos
DTitulos = {
  'Campones':  Titulo('Campones', 'Capital', 0, 'null','null'),
  'Barao':     Titulo('Barao', '', 1, '', ''),
  'Nobre':     Titulo('Nobre', '', 2, '', ''),
  'Moeda':     Titulo('Mestre da moeda', '', 5, '', ''),
  'Marechal':  Titulo('Marechal', '', 5, '', ''),
  'Espiao':    Titulo('Mestre da espionagem', '', 5, '', ''),
  'Capelao':   Titulo('Capelao', '', 5, '', ''),
  'Chanceler': Titulo('Chanceler', '', 6, '', ''),
  'Conde':     Titulo('Conde', '', 7, '', ''),
  'Duque':     Titulo('Duque', '', 8, '', ''),
  'Rei':       Titulo('Rei', '', 9, '', ''),
  'Imperador': Titulo('Imperador', '', 10, '', 'null')
}

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

    elif mensagem[1] in ['95', 'ocupacoes', 'o']:
      #95 Ocupacoes - Edicao e criacao de ocupacoes
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
      print (DOcupacoes)

    elif mensagem[1] in ['0','00','conta','c']:
      #0 Conta
      await conta_handler(str(message.author.id), mensagem, message)

    #? Ajuda
    else:
      await message.channel.send('```Precisa de ajuda?\n' + \
      '1. perfil/p - Exibe as informacoes do seu personagem.\n'+ \
      '95. ocupacoes/o - Edicao e criacao de ocupacoes\n' + \
      '96. meudb - Printa seu proprio db no console.\n' + \
      '97. sistema - Printa as informacoes de sistema.\n' + \
      '98. console - Printa a lista de ocupacoes no console.\n'+ \
      '00. conta/c - Cadastro e opcoes de conta.' + \
      '```')

  await controlador_de_tempo()
  
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
  #1 Meu perfil: Ok
  if mensagem[2] in ['1', 'recursos', 'r']:
    #1.1 Meu perfil - Recursos
    await perfil_recursos(author_id, message)
  elif mensagem[2] in ['2', 'ocupacao', 'o']:
    #1.2 Meu perfil - Mudar de ocupacao
    await perfil_ocupacao(author_id, mensagem)
  elif mensagem[2] in ['3', 'familia', 'f']:
    #1.3 Meu perfil - Minha familia
    await perfil_familia(author_id, mensagem, message)
  else:
    #1.? Meu perfil - Ajuda
    await message.channel.send('```Meu perfil\n'+ \
    '1. recursos/r - Mostra os recursos que voce possui.\n'+ \
    '2. ocupacao/o - Permite trocar de ocupacao.\n'+ \
    '3. familia/f - Ver informacoes da minha familia\n' + \
    '```')

async def perfil_recursos(author_id, message) -> None:
  #1.1 Meu perfil - Recursos: Ok
  author = load(author_id)
  await message.channel.send('```Meu perfil\n'+ \
    author.titulo[0] + ' ' + \
    author.nome + ': ' + \
    author.ocupacao + \
    '\n\nOuro: ' + str(author.recursos.ouro)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.ouro)+')' + \
    '\nPrestigio: ' + str(author.recursos.prestigio)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.prestigio) + ')' + \
    '\nDevocao: ' + str(author.recursos.devocao)+ ' +(' + \
    str(DOcupacoes[author.ocupacao].recursos.devocao)+ ')' + \
    '\nRenome: +(' + \
    str(DOcupacoes[author.ocupacao].recursos.renome)+ ')' + \
    '```')

async def perfil_ocupacao(author_id, mensagem) -> None:
  #1.2 Meu perfil - Ocupacao: Ok
  if (mensagem[3] in DOcupacoes):
    #1.2.X Meu perfil - Mudar de ocupacao - Ocupacao escolhida: Ok
    author = load(author_id)
    author.ocupacao = DOcupacoes[mensagem[3]].nome
    db[author_id] = dump(author)
    await message.channel.send('```Sua ocupacao mudou.\n' + \
    'Agora voce e: ' + \
    DOcupacoes[mensagem[3]].nome + \
    '```')
  else:
    #1.2.? Meu perfil - Mudar de ocupacao - Ajuda: Ok
    await message.channel.send('```Lista de ocupacoes```')
    await message.channel.send (DOcupacoes)

async def perfil_familia(author_id, mensagem, message) -> None:
  #1.3 Meu perfil - Minha familia
  DFamilias= load('familias')
  if mensagem[3] in ['1', 'membros', 'm']:
    #1.3.1 Meu perfil - Minha familia - Membros
    if (author.familia == ''):
      return
    await message.channel.send( DFamilias[author.familia].membros)
  elif mensagem[3] in ['2', 'chefe', 'c']:
    #1.3.2 Meu Perfil - Minha familia - Chefe
    if (author.familia == ''):
      return await message.channel.send("```Você ainda não pertence a nenhuma familia.\nJunte-se a uma das familias existentes ou crie a sua!```")
    await message.channel.send( DFamilias[author.familia].chefe)
  elif mensagem[3] in ['9', 'juntar', 'j']:
    #1.3.9 Meu perfil - Minha familia - Ser adotado
    if mensagem[4] in DFamilias:
      if (DFamilias[author.familia].chefe == author):
        DFamilias[mensagem[4]].renome += int(DFamilias[author.familia].renome / 2)
        if(DFamilias[author.familia].membros):
          DFamilias[author.familia].chefe = DFamilias[author.familia].membros[0]
          pop(DFamilias[author.familia].membros[0])
          DFamilias[author.familia].renome = int(DFamilias[author.familia].renome/2)
        elif (author.id in DFamilias[author.familia].membros):
          for i in DFamilias[author.familia].membros:
            if DFamilias[author.familia].membros[i] == author:
              pop(DFamilias[author.familia].membros[i])
      author.familia = mensagem[4]
      DFamilias[mensagem[4]].membros.append(author)
      
    else:
      await message.channel.send(DFamilias)
  elif mensagem[3] in ['0','criar']:
    #1.3.0 Meu perfil - Minha familia - Criar uma familia
    if mensagem[4] in DFamilias:
      await message.channel.send('```Esse nome de familia já existe.```')
    elif mensagem[4] in ['?']:
      await message.channel.send('```Escolha um sobrenome para a familia.```')
    else:
      DFamilias[mensagem[4]] = Familia(mensagem[4],0,author,[])
      db['familias'] = dump(DFamilias)
      await message.channel.send('```Familia criada com sucesso.```')
      
    
  else:
    await message.channel.send('```Minha familia:\n' + \
    '1. membros/m - Mostra a lista de membros da sua familia\n' + \
    '2. chefe/c - Mostra quem e o chefe da sua familia\n' + \
    '9. juntar/j - Se juntar a uma familia ja existente\n' + \
    '0. criar - Cria uma nova familia' + \
    '```')
      
async def ocupacoes_handler(author, mensagem, message) -> None:
  #95 Ocupacoes
  if mensagem [2] in ['1', 'criar', 'c']:
    #95.1 Ocupacoes - Criar
    await ocupacoes_criar(mensagem)
  elif mensagem[2] in ['2', 'lista', 'l']:
    #95.2 Ocupacoes - Lista
    await ocupacoes_lista(mensagem, message)
  else:
    #95.? Ocupacoes - Ajuda
    await message.channel.send('```Ocupacoes\n' + \
    '1. criar/c - Cria uma nova ocupacao\n' + \
    '2. lista/l - Mostra a lista de ocupacoes\n' + \
    '0. apagar/a - Apaga uma ocupacao' + \
    '```')
    
async def ocupacoes_criar(mensagem) -> None:
  #95.1 Ocupacoes - Criar: Ok
  DOcupacoes = load('ocupacoes')
  nova_ocupacao = Ocupacao(mensagem[3], int(mensagem[4]), Recursos(int(mensagem[5]), int(mensagem[6]), int(mensagem[7]), int(mensagem[8])))
  DOcupacoes[mensagem[3]] = nova_ocupacao
  db['ocupacoes'] = dump(DOcupacoes)
  await message.channel.send("```Ocupacao criada com sucesso.```")

async def ocupacoes_lista(mensagem, message) -> None:
  #95.2 Ocupacoes - Lista: NotOk
  ocupacoes = load('ocupacoes')
  for i in ocupacoes:
    lista.append(ocupacoes[i].nome)
  await message.channel.send(lista)

async def ocupacoes_apagar(mensagem) -> None:
  #95.0 Ocupacoes - Apagar: Ok
  DOcupacoes.pop(mensagem[3])
  db['ocupacoes'] = dump(DOcupacoes)
  await message.channel.send("```Ocupacao apagada com sucesso.```")
  
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
  await message.channel.send('```Conta criada/resetada com sucesso.```')

async def conta_apagar(author_id, message):
  #0.0 Conta - Apagar conta: Ok
  del db[str(author_id)]
  await message.channel.send('```Conta apagada com sucesso.```')
  
def load(coisa):
  return pickle.loads(db[coisa].encode('latin1'))
  
def dump(coisa):
  return pickle.dumps(coisa).decode('latin1')
  
def lucro_profissao():
  # Gera recursos para os jogadores: NotOk
  # Mas parece estar ficando bom
  DFamilias = load('familias')
  for chave in db.keys():
    if chave not in ['sistema', 'ocupacoes', 'familias', 'titulos']:
      usuario = load(chave)
      usuario.recursos.ouro += DOcupacoes[usuario.ocupacao].recursos.ouro
      usuario.recursos.prestigio += DOcupacoes[usuario.ocupacao].recursos.prestigio
      usuario.recursos.devocao += DOcupacoes[usuario.ocupacao].recursos.devocao
      DFamilias[usuario.familia].renome = usuario.recursos.renome
      db[chave] = dump(usuario)
  db['familias'] = dump(DFamilias)

client.run(os.environ['DATABASE_PASSWORD'])
# Senha do DB