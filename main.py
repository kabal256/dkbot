import discord
import os
import struct
import requests
import json
import asyncio
import pytz
from replit import db
from datetime import datetime, timezone

client = discord.Client()

# Variaveis Inicializadas ---------------------------------------------------------------

#Configuracao do horario

set(pytz.all_timezones_set)
tz = pytz.timezone('America/Cuiaba')

# Listas --------------------------------------------------------------------------------


# Variáveis sistêmicas armazenadas no bd
# Horas, Ban no pato
db['s'] = [0,0]

# Famílias
# Membros[], Renome Total
# ['f'] = [ [ ['Nome da família', 'Nome do Patriarca'], [ID dos membros da família] ] ]
db['f'] = [ [ ['', ''], ['227209279260590080', '284799007384141825', '320782054964985869', '281238791203717131'] ] ]

# Renome, Ouro, Prestigio, Devocao, Nome da Ocupacao
vLista_de_ocupacoes = [ [0, 1, 0, 0, '0Desocupado'], [0, 3, 1, 3, '1Fazendeiro'] ]
#, '2. Lenhador', '3. Marceneiro', '4. Minerador', '5. Ferreiro', '6. Ladrao', '7. Mercenario', '8. Herbalista']

vLista_de_titulos = ['Campones', 'Nobre', 'Barao', 'Conde', 'Duque', 'Rei', 'Imperador']

# Objetos -------------------------------------------------------------------------------
class Recursos:
  # self, int, int, int
  def __init__(self, ouro, prestigio, devocao):
    self.ouro = ouro
    self.prestigio = prestigio
    self.devocao = devocao
class Ocupacao:
  # self, int, class
  def __init__(self, nome, tier, recursos):
    self.nome = nome
    self.tier = tier
    self.recursos = recursos
class Familia:
  # self, string, int, array[id(string)]
  def __init__(self, nome, renome, membros):
    self.nome = nome
    self.renome = renome
    self.membros = membros
class Titulo:
  # self, string, int, id(string)
  def __init__(self, nome, tier, dono):
    self.nome = nome
    self.tier = tier
    self.dono = dono
class Usuario:
  # self, string, string, class, string, string, array[class]
  def __init__(self, id, nome, recursos, ocupacao, familia, titulo):
    self.id = id
    self.nome = nome
    self.recursos = recursos
    self.ocupacao = ocupacao
    self.familia = familia
    self.titulo = titulo

# Inicializador de usuário manual -------------------------------------------------------
# Atualização do DB:
# 0. Recursos
# 0.0. Renome,  0.1. Ouro,        0.2. Prestígio, 0.3. Devoção,
# 1. Adereçamento
# 1.0 Ocupacao, 1.1 Título,       1.2 Família
# 2. Identificação
# 2.0 Nome,     2.1 Discriminator

#db[ID] [ [Renome, Ouro, Prestígio, Devoção], [Ocupacao, Título, Família], [Nome, Discriminator] ]

#del db['227209279260590080'] #= [ [0, 10, 0, 0], [0, 0, 0], ["Kabal", "5415"] ]
#del db['284799007384141825'] #= [ [0, 10, 0, 0], [0, 0, 0], ["June", "5109"] ]
#del db['320782054964985869'] #= [ [0, 10, 0, 0], [0, 0, 0], ["Valman", "2329"] ]
#del db['281238791203717131'] #= [ [0, 10, 0, 0], [0, 0, 0], ["Soldier", "9850"] ]

# Evento - Ao iniciar -------------------------------------------------------------------

@client.event
async def on_ready():
  print("{0.user} está online.\nDeixe os reinos cairem...".format(client))
  await controlador_de_tempo()

# Evento - Quando alguém entra no servidor ----------------------------------------------

@client.event
async def on_member_join(member):
  if (db[str(member.id)] == member.id):
    print('Seja bem vindo de volta, '+{member.nick}+'.')
    return

  else:
    await message.channel.send('Seja bem vindo, '+{member.nick}+'.\n' + \
    'Digite **vsf** em #comandos para mais informacoes.')
  await controlador_de_tempo()

# Evento - Ao chamar o bot --------------------------------------------------------------

@client.event
async def on_message(message):
  if (message.author == client.user):
    return

  #0 Menu Principal
  mensagem = message.content.split(' ',)
  mensagem += '?'
  if mensagem[0] == 'vsf':
    #1 Meu perfil
    if mensagem[1] in ['1', 'perfil', 'p']:
      #1.1 Meu perfil - Meus recursos
      if mensagem[2] in ['1', 'recursos', 'r']:
        await message.channel.send('```Meu perfil\n'+ \
          vLista_de_titulos[        db[str(message.author.id)][1][1] ]+ ' ' + \
                                    db[str(message.author.id)][2][0]+ \
          ': '+vLista_de_ocupacoes[ db[str(message.author.id)][1][0] ][4]+ \
          '\nRenome: '+         str(db[str(message.author.id)][0][0])+ ' (+' + \
          str(vLista_de_ocupacoes[  db[str(message.author.id)][1][0] ][0]) + ')' + \
          '\nOuro: '+           str(db[str(message.author.id)][0][1])+ ' (+' + \
          str(vLista_de_ocupacoes[  db[str(message.author.id)][1][0] ][1]) + ')' + \
          '\nPrestigio: '+      str(db[str(message.author.id)][0][2])+ ' (+' + \
          str(vLista_de_ocupacoes[  db[str(message.author.id)][1][0] ][2]) + ')' + \
          '\nDevocao: '+        str(db[str(message.author.id)][0][3])+ ' (+' + \
          str(vLista_de_ocupacoes[  db[str(message.author.id)][1][0] ][3]) + ')' + \
          '```')

      #1.2 Meu perfil - Mudar de ocupacao
      elif mensagem[2] in ['2', 'ocupacao', 'o']:
        #1.2.? Meu perfil - Mudar de ocupacao - Nenhuma escolha
        if (mensagem[3]=='?'):
          await message.channel.send('```Lista de ocupacoes```')
          await message.channel.send (vLista_de_ocupacoes)

        #1.2.X Meu perfil - Mudar de ocupacao - Ocupacao escolhida
        elif (int(mensagem[3])<=len(vLista_de_ocupacoes) and int(mensagem[3])>=0):
          db[str(message.author.id)][1][0]=int(mensagem[3])
          await message.channel.send('```Sua ocupacao mudou.\n' + \
          'Agora voce e: '+ \
          vLista_de_ocupacoes[int(mensagem[3])][4]+'```')

        #1.2.!X Meu perfil - Mudar de ocupacao - Ajuda
        else:
          await message.channel.send('```Lista de ocupacoes```')
          await message.channel.send (vLista_de_ocupacoes[4])
          
      #1.? Meu perfil - Ajuda
      else:
        await message.channel.send('```Meu perfil\n'+ \
        '1. recursos/r - Mostra os recursos que voce possui.\n'+ \
        '2. ocupacao/o - Permite trocar de ocupacao.\n'+ \
        '```')

    #2 Lugares
    elif mensagem[1] in ['2', 'lugares', 'l']:
      print('Nao ta implementado ainda.')
      #2.1 Lugares - Onde estou
        #2.1.1 Lugares - Onde estou - Cidade (1/3)
        #2.1.2 Lugares - Onde estou - Igreja (0/3)
        #2.1.3 Lugares - Onde estou - Baronato (0/3)
        #2.1.4 Lugares - Onde estou - Capital (0/5)
      #2.2 Lugares - Terras (0/12)
        #2.2.0 Lugares - Terras - 0 Capital
        #2.2.X Lugares - Terras - 1-12 (Vazio)
      #2.3 Lugares - 

    #96 Teste - Printa seu próprio db
    elif mensagem[1] in ['96', 'seudb']:
      print(db[str(message.author.id)])
        
    #97 Teste - Printa as informacoes de sistema
    elif mensagem[1] in ['97', 'sistema']:
      print (db['s'])

    #98 Teste - Printa a lista de ocupacoes no console
    elif mensagem[1] in ['98','console']:
      aux = 0
      for i in vLista_de_ocupacoes:
        print (vLista_de_ocupacoes[aux][4])
        aux += 1
    
    #99 Teste - Ban no pato
    elif mensagem[1] in ['99','pato']:
      db['s'][1]+=1
      await message.channel.send('Ban no pato. Voce baniu o pato ' + \
      'Total de bans: '+str(db['s'][1]))
      if str(db['s'][1]) == '69':
        await message.channel.send('Nice.')

    #0 Conta
    elif mensagem[1] in ['0','00','conta','c']:
      #0.1 Conta - Cadastro / Reset
      #db[ID] [ [Renome, Ouro, Prestígio, Devoção], [Ocupacao, Título, Família], [Nome, Discriminator] ]
      if mensagem[2] in ['1','cadastro','reset']:
        db[str(message.author.id)] = [ [0, 10, 0, 0], [0, 0, 0], [message.author.name, message.author.discriminator] ]
        await message.channel.send('```Conta criada/resetada com sucesso.```')

      #0.0 Conta - Apagar conta
      elif mensagem[2] in ['0', 'apagar']:
        del db[str(message.author.id)]
        await message.channel.send('```Conta apagada com sucesso.```')
        
      else:
        await message.channel.send('```Minha conta\n'+ \
        '1. cadastro/reset - Resets nao podem ser revertidos.\n' + \
        '0. apagar - Essa acao exclui a sua conta.')

    #? Ajuda
    else:
      await message.channel.send('```Precisa de ajuda?\n' + \
      '1. perfil/p - Exibe as informacoes do seu personagem.\n'+ \
      '96. seudb - Printa seu proprio db no console.\n' + \
      '97. sistema - Printa as informacoes de sistema.\n' + \
      '98. console - Printa a lista de ocupacoes no console.\n'+ \
      '99. pato - Ban no pato.\n' + \
      '00. conta/c - Cadastro e opcoes de conta.```')

  await controlador_de_tempo()

# Funções -------------------------------------------------------------------------------

#1 Evita spam - Não funcionando
  
async def evita_spam():
  intervalo_de_tempo = int(time.time())

#2 Controlador de tempo
  
async def controlador_de_tempo():
  while True:
    horario = datetime.now(tz=tz)
    if db['s'][0] != horario.hour:
      if db['s'][0] < 23:
        proxima_hora = db['s'][0] + 1
      else:
        proxima_hora = 1
      db['s'][0] = horario.hour
      lucro_profissao()
    else:
      await asyncio.sleep(60)

#3 Adiciona recursos

def lucro_profissao():
  for chave in db.keys():
    if db[chave] != db['s'] or db[chave] != db['f']:
      db[chave][0][0] += vLista_de_ocupacoes[ db[chave][1][0] ][0]
      db[chave][0][1] += vLista_de_ocupacoes[ db[chave][1][0] ][1]
      db[chave][0][2] += vLista_de_ocupacoes[ db[chave][1][0] ][2]
      db[chave][0][3] += vLista_de_ocupacoes[ db[chave][1][0] ][3]
#----------------------------------------------------------------------------------------

client.run(os.environ['DATABASE_PASSWORD'])
