from multiprocessing.dummy import connection
from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests
import sqlite3
connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Calculadora
    if message.content.startswith('!calc'):
        operacion = message.content.split (' ')[1]

        def calc(op):
            if op.__contains__('+'):
                num1 = int(op.split('+')[0])
                num2 = int(op.split('+')[1])
                return num1 + num2;
            elif op.__contains__('-'):
                num1 = int(op.split('-')[0])
                num2 = int(op.split('-')[1])
                return num1 - num2;
            elif op.__contains__('x'):
                num1 = int(op.split('x')[0])
                num2 = int(op.split('x')[1])
                return num1 * num2;
            elif op.__contains__('/'):
                num1 = int(op.split('/')[0])
                num2 = int(op.split('/')[1])
                return num1 / num2;
            else:
                return 'Ha habido un error'
        resultado = calc(operacion);

        await message.channel.send(f'Hola <@{message.author.id}>')
        await message.channel.send(f'el resultado es: {resultado}')

    #criptomoneda
    if message.content.startswith('$cryto'):
        moneda = message.content.split(' ')[1]
        divisa = message.content.split(' ')[2]
        info = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={moneda}&tsyms={divisa}')

        response = info.json()
        price = response['DISPLAY'][moneda][divisa]['PRICE']
        high = response['DISPLAY'][moneda][divisa]['HIGH24HOUR']
        low = response['DISPLAY'][moneda][divisa]['LOW24HOUR']

        await message.channel.send(f'Moneda: {divisa}, Cryptomoneda: {moneda}')
        await message.channel.send(f'El precio: {price}')
        await message.channel.send(f'Precio más alto: {high}')
        await message.channel.send(f'Precio más bajo: {low}')


    #clima
    if message.content.startswith('!clima'):
        ciudad = message.content.split(' ')[1]
        info = requests.get(f'https://goweather.herokuapp.com/weather/{ciudad}')

        response = info.json()
        todayTemp = response['temperature']
        tomorrowTemp = response['forecast'][0]['temperature']
        tomorrow2Temp = response['forecast'][1]['temperature']

        await message.channel.send(f'Temperatura en: {ciudad}')
        await message.channel.send(f'El dia de hoy es: {todayTemp}')
        await message.channel.send(f'El dia de mañana sera: {tomorrowTemp}')
        await message.channel.send(f'El dia de pasado mañana sera: {tomorrow2Temp}')

    #paises


    #Crear un Usuario 
    if message.content.startswith('!CrearUsuario'):
        first_name = message.content.split(' ')[1]
        last_name = message.content.split(' ')[2]
        full_name = f'{first_name} {last_name}'
        cur.execute('INSERT INTO users (discord_id, name) VALUES (?, ?)', [message.author.id, full_name])
        connectionDB.commit()
        await message.channel.send('Usuario Creado!')

        
    #Eliminar un Usuario
    if message.content.startswith('!BorrarUsuario'):
        cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
        connectionDB.commit()
        await message.channel.send('Usuario Eliminado!')

    




client.run(os.environ['TOKEN'])