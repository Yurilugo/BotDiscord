import tempfile
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
    if message.content.startswith('!pais'):
        if len(message.content) > 5:
            pais = message.content.split(' ')[1]

            infoPais = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
            responsePais = infoPais.json()
            bandera = responsePais[0]['flags']['png'] 
            nombre = responsePais[0]['name']['common']
            capital = responsePais[0]['capital'][0]
            region = responsePais[0]['region']
            poblacion = responsePais[0]['population']


            infoClima = requests.get(f'https://weatherdbi.herokuapp.com/data/weather/{pais}')
            responseClima = infoClima.json()
            hora = responseClima['currentConditions']['dayhour']
            temperatura = responseClima['currentConditions']['temp']['c']
            clima = responseClima['currentConditions']['comment']
            climaimg = responseClima['currentConditions']['iconURL']


            await message.channel.send(f'Hello, <@{message.author.id}>')
            await message.channel.send(bandera)
            await message.channel.send(f'Country :  {nombre}')
            await message.channel.send(f'Capital :  {capital}')
            await message.channel.send(f'Region : {region}')
            await message.channel.send(f'Population : {poblacion}')
            await message.channel.send(f'Day and hour :  {hora}')
            await message.channel.send(f'Temperature at this time :  {temperatura}°C')
            await message.channel.send(f'The weather at this time :  {clima}')
            await message.channel.send(climaimg)

        else:
            ip =  requests.get(f'https://api.geoapify.com/v1/ipinfo?&apiKey=66931cf4d4bd40259dafee5d6d898138')
            response_ip = ip.json()
            paisIp = response_ip['country']['names']['de']


            infoPais = requests.get(f'https://restcountries.com/v3.1/name/{paisIp}')
            responsePais = infoPais.json()
            bandera = responsePais[0]['flags']['png'] 
            nombre = responsePais[0]['name']['common']
            capital = responsePais[0]['capital'][0]
            region = responsePais[0]['region']
            poblacion = responsePais[0]['population']


            infoClima = requests.get(f'https://weatherdbi.herokuapp.com/data/weather/{paisIp}')            
            responseClima = infoClima.json()
            hora = responseClima['currentConditions']['dayhour']
            temperatura = responseClima['currentConditions']['temp']['c']
            clima = responseClima['currentConditions']['comment']
            climaimg = responseClima['currentConditions']['iconURL']


            await message.channel.send(f'Hello, <@{message.author.id}>')
            await message.channel.send(bandera)
            await message.channel.send(f'Country :  {nombre}')
            await message.channel.send(f'Capital :  {capital}')
            await message.channel.send(f'Region : {region}')
            await message.channel.send(f'Population : {poblacion}')
            await message.channel.send(f'Day and hour :  {hora}')
            await message.channel.send(f'Temperature at this time :  {temperatura}°C')
            await message.channel.send(f'The weather at this time :  {clima}')
            await message.channel.send(climaimg)



    #Crear un Usuario 
    if message.content.startswith('!CrearUsuario'):
        first_name = message.content.split(' ')[1]
        last_name = message.content.split(' ')[2]
        full_name = f'{first_name} {last_name}'
        # email = message.content.split(' ')[3]
        # password = message.content.split(' ')[4]
        # confirm_pass = message.content.split(' ')[5]

        # response = requests.post('http://api.cup2022.ir/api/v1/user',
        # data={'name': full_name, 'email': email, 'password': password, 'passwordConfirm': confirm_pass})


        cur.execute('INSERT INTO users (discord_id, name) VALUES (?, ?)', [message.author.id, full_name])
        connectionDB.commit()
        await message.channel.send('Usuario Creado!')


    #Eliminar un Usuario
    if message.content.startswith('!BorrarUsuario'):
        cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
        connectionDB.commit()
        await message.channel.send('Usuario Eliminado!')

    




client.run(os.environ['TOKEN'])