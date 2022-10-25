from datetime import date
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

    #info de beisboll

    #Info del jugador
    def JugadorID(full_name):
        info = requests.get(f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{full_name}%25%27')
        responseIp = info.json()
        JugadorID = responseIp['search_player_all']['queryResults']['row']['player_id']
        return JugadorID


    if message.content.startswith('!jugador'):
        nameJugador = message.content.split(' ')[1]
        lastJugador = message.content.split(' ')[2]
        full_name = f'{nameJugador} {lastJugador}'
        ResultId = JugadorID(full_name)

        p = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{ResultId}/headshot/67/current"

        infoJugador = requests.get(f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{ResultId}'")
        responseJugador = infoJugador.json()

        Jugador = responseJugador['player_info']['queryResults']['row']['name_display_last_first']
        Nacionalidad = responseJugador['player_info']['queryResults']['row']['birth_country']
        Nacimiento = responseJugador['player_info']['queryResults']['row']['birth_date']
        Ciudad = responseJugador['player_info']['queryResults']['row']['birth_city']
        Altura = responseJugador['player_info']['queryResults']['row']['height_feet']
        Edad = responseJugador['player_info']['queryResults']['row']['age']
        Peso = responseJugador['player_info']['queryResults']['row']['weight']
        EquipoActual = responseJugador['player_info']['queryResults']['row']['team_name']
        bateo = responseJugador['player_info']['queryResults']['row']['bats']
        posicion = responseJugador['player_info']['queryResults']['row']['primary_position_txt']
        twitter = responseJugador['player_info']['queryResults']['row']['twitter_id']
        debut = responseJugador['player_info']['queryResults']['row']['pro_debut_date']
       
        date = Nacimiento.split('T')[0]
        date_debut = debut.split('T')[0]
        #weight in kg
        weight_kg = int(Peso) / 2.205
        kg_round = round(weight_kg, 2)
        #height in m
        height_m = int(Altura) / 3.281
        m_round = round(height_m, 2)


        await message.channel.send(f'{p}')
        await message.channel.send(f'Apellido, Nombre: {Jugador}')
        await message.channel.send(f'Nacionalidad: {Nacionalidad}')
        await message.channel.send(f'Ciudad: {Ciudad}')
        await message.channel.send(f'Nacimiento: {date}')
        await message.channel.send(f'Edad: {Edad}')
        await message.channel.send(f'Altura: {m_round}')
        await message.channel.send(f'Peso: {kg_round}')
        await message.channel.send(f'Equipo Actua: {EquipoActual}')
        await message.channel.send(f'Debuto en: {date_debut}')  
        await message.channel.send(f'Batea en el perfil: {bateo}')
        await message.channel.send(f'Juega en: {posicion}')
        await message.channel.send(f'Su twitter es: {twitter}')
    
    
    if message.content.startswith('!estadisticas'):

        nameJugador = message.content.split(' ')[1]
        lastJugador = message.content.split(' ')[2]
        year =  message.content.split(' ')[3]
        full_name = f'{nameJugador} {lastJugador}'
        result_id = JugadorID(full_name)
        p = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"   
        details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='{year}'&player_id='{result_id}'")
        response_career = details.json()
        
        Hits = response_career['sport_hitting_tm']['queryResults']['row']['h']
        HomeRun = response_career['sport_hitting_tm']['queryResults']['row']['hr']
        Carreras = response_career['sport_hitting_tm']['queryResults']['row']['r']
        Ponches = response_career['sport_hitting_tm']['queryResults']['row']['so']
        BasexBola = response_career['sport_hitting_tm']['queryResults']['row']['bb']
        Avg = response_career['sport_hitting_tm']['queryResults']['row']['avg']
        TurnoAlBate  = response_career['sport_hitting_tm']['queryResults']['row']['ab']
        Jjugados = response_career['sport_hitting_tm']['queryResults']['row']['g']
        CarreraImpulsada = response_career['sport_hitting_tm']['queryResults']['row']['rbi'] 
        Season = response_career['sport_hitting_tm']['queryResults']['row']['season']

        await message.channel.send(f'{p}')
        await message.channel.send(f'Temporada: {Season}')
        await message.channel.send(f'Juegos jugados: {Jjugados} ')
        await message.channel.send(f'Turnos al bate: {TurnoAlBate}')
        await message.channel.send(f'Carreras: {Carreras}')
        await message.channel.send(f'Hits: {Hits}')
        await message.channel.send(f'Carrara impulsada: {CarreraImpulsada}')
        await message.channel.send(f'Base por bola: {BasexBola}')
        await message.channel.send(f'Ponches: {Ponches}')
        await message.channel.send(f'HomeRuns: {HomeRun}')
        await message.channel.send(f'PRO: {Avg}') 



        

        














           














client.run(os.environ['TOKEN'])



    # #Crear un Usuario 
    # if message.content.startswith('!CrearUsuario'):
    #     first_name = message.content.split(' ')[1]
    #     last_name = message.content.split(' ')[2]
    #     full_name = f'{first_name} {last_name}'
    #     email = message.content.split(' ')[3]
    #     password = message.content.split(' ')[4]
    #     confirm_pass = message.content.split(' ')[5]

    #     # response = requests.post('http://api.cup2022.ir/api/v1/user', 
    #     # data={'name': full_name, 'email': email, 'password': password, 'passwordConfirm': confirm_pass})


    #     cur.execute('INSERT INTO users (discord_id, name, email, password) VALUES (?, ?, ?, ?))', [message.author.id, full_name, email, password])
    #     connectionDB.commit()
    #     await message.channel.send('Usuario Creado!')


    # #Eliminar un Usuario
    # if message.content.startswith('!BorrarUsuario'):
    #     cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
    #     connectionDB.commit()
    #     await message.channel.send('Usuario Eliminado!')