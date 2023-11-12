from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import requests
from datetime import datetime


# TOKEN DE LA API
API_KEY = 'f76d099656msh18868140725a6d9p1190dfjsn26c4fa77f2c8'

# URL DE LA API
API_URL = "https://ergast.com/api/f1/2023.json"

# TOKEN DEL BOT
TOKEN = '6916160737:AAEym5bUZb6CqG3KBfV9Xbc9irplSBc3MKo'

#ID GRUPO TELEGRAM
TU_ID_DE_GRUPO = -2066532865

# Variable de estado para rastrear si el bot ha sido iniciado
bot_iniciado = False


# ---------- INICIAR BOT ----------

def iniciar_bot(update: Update, context: CallbackContext) -> None:
    global bot_iniciado
    
    bot_iniciado = True
    update.message.reply_text('Bot iniciado. ¡Listo para recibir comandos!')


# ---------- SALUDO ----------

def saludo(update: Update, context: CallbackContext) -> None:
    if bot_iniciado:
        update.message.reply_text('¡Hola, Soy Fernando Alonso! Piloto español y bicampeón del mundo de F1 🏆🏆')
    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')


# ---------- SALUDAR USUARIO ----------

def saludar_usuario(update: Update, context: CallbackContext):
    
    mensaje_usuario = update.message.text.lower()
    saludos = ["hola", "saludos", "¡hola!", "¡saludos!", "buenas", "buenas!"]

    # VERIFICA SI EL MENSAJE DEL USUARIO ES ALGUNA DE ESTAS PALABRAS
    if any(saludo in mensaje_usuario for saludo in saludos):
        respuesta_saludo = random.choice(["¡Hola!", "¡Saludos!", "¡Hola, compañero!", "¡Hola a todos!", "¡Buenas!", "¡Buenos nanodías!"])
        update.message.reply_text(respuesta_saludo)



# ---------- GENERAR MENSAJE ----------

gramatica_mensaje = {
"<mensaje>": ["<nombre> <verbo> <numero> <complemento> <gp>"],

"<nombre>": ["Fernando Alonso", "El asturiano", "El samurái"],
"<verbo>": ["logra", "consigue"],
"<numero>": ["un"],
"<complemento>": ["podio mágico", "histórico podio", "clasificación espectacular"],
"<gp>": ["en el Gran Premio de Australia", "en el Gran Premio de Miami", "en el Gran Premio de Spa", "en el Gran Premio de Monza", "en el Gran Premio de Brasil"]

}

def generar_mensaje(update: Update, context: CallbackContext):
    global bot_iniciado

    if bot_iniciado:
        #Genera una frase a partir de un símbolo no terminal utilizando la gramática definida.
        mensaje_generado = generar_frase("<mensaje>")
        update.message.reply_text(mensaje_generado)
    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')

def generar_frase(simbolo):
    if simbolo not in gramatica_mensaje:  # Si es un símbolo terminal, simplemente se devuelve
        return simbolo

    # Seleccionar una producción aleatoria para el símbolo
    produccion = random.choice(gramatica_mensaje[simbolo])

    # Dividir la producción en sus componentes y generar la frase para cada componente
    return " ".join(generar_frase(comp) for comp in produccion.split())



# ---------- NUEVO MIEMBRO ----------

def on_new_member(update: Update, context: CallbackContext):
    # OBTIENE LA LISTA DE NUEVOS MIEMBROS
    new_members = update.message.new_chat_members

    # ENVÍA UN MENAJE DE BIENVENIDA AL USUARIO
    for member in new_members:
        update.message.reply_text(f"¡Bienvenido al grupo, {member.first_name}!")



# ---------- ÚLTIMA CARRERA ----------

def ultima_carrera(update: Update, context: CallbackContext) -> None:
    global bot_iniciado

    if bot_iniciado:
        # OBTIENE LA FECHA DEL SISTEMA
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        def obtener_posicion(carrera, driver_id):
            for resultado in carrera['Results']:
                if resultado['Driver']['driverId'] == driver_id:
                    return resultado['position']
            return "No disponible"

        try:
            # OBTIENE L AINFORMACIÓN DE LA ÚLTIMA CARRERA DE FERNANDO ALONSO
            url = f"http://ergast.com/api/f1/current/drivers/alonso/results.json"
            response = requests.get(url).json()

            # OBTIENE LA ÚLTIMA CARRERA EN LA QUE PARTICIPÓ
            carrera_actual = None
            for carrera in response['MRData']['RaceTable']['Races']:
                if carrera['date'] <= fecha_actual:
                    carrera_actual = carrera
                else:
                    break

            if carrera_actual:
                nombre_carrera = carrera_actual['raceName']
                fecha_carrera = carrera_actual['date']
                circuito = carrera_actual['Circuit']['circuitName']
                
                # OBTIENE LA POSICIÓN DE PARRILLA
                parrilla = obtener_posicion(carrera_actual, 'alonso')

                # OBTIENE LA POSICIÓN FINAL DE CARRERA
                posicion_final = obtener_posicion(carrera_actual, 'alonso')

                mensaje_respuesta = f"Mi última carrera durante el {nombre_carrera} en el circuito '{circuito}' el día {fecha_carrera}.\n\nSalí en {parrilla} posición y acabé {posicion_final}º"

                update.message.reply_text(mensaje_respuesta)
            else:
                update.message.reply_text("Fernando Alonso no ha participado en ninguna carrera en la temporada actual.")

        except Exception as e:
            print(f"Error al procesar la respuesta de la API: {e}")
            update.message.reply_text("Lo siento, no pude obtener la información sobre la última carrera de Fernando Alonso en este momento.")
    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')



# ---------- PRÓXIMAS CARRERAS ----------

def proximas_carreras(update: Update, context: CallbackContext) -> None:
    global bot_iniciado

    if bot_iniciado:
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        try:
            # OBTIENE LA INFROMACIÓN DE LAS PRÓXIMAS CARRERAS
            url = f"http://ergast.com/api/f1/2023.json"
            response = requests.get(url).json()

            # OBTIENE LAS CARRERAS A PARTIR DE LA FECHA ACTUAL
            proximas_carreras = []
            for carrera in response['MRData']['RaceTable']['Races']:
                if carrera['date'] > fecha_actual:
                    proximas_carreras.append(carrera)
    

            if proximas_carreras:
                mensaje_respuesta = "Mis próximas carreras son:\n\n"
                for carrera in proximas_carreras:

                    round = carrera['round']
                    nombre_carrera = carrera['raceName']
                    circuito = carrera['Circuit']['circuitName']

                    fecha_entrenamientos1 = carrera['FirstPractice']['date']
                    hora_entrenamientos1 = carrera['FirstPractice']['time']

                    fecha_entrenamientos2 = carrera['SecondPractice']['date']

                    hora_entrenamientos2 = carrera['SecondPractice']['time']

                    fecha_entrenamientos3 = carrera['ThirdPractice']['date']
                    hora_entrenamientos3 = carrera['ThirdPractice']['time']

                    fecha_clasificacion = carrera['Qualifying']['date']
                    hora_clasificacion = carrera['Qualifying']['time']


                    fecha_carrera = carrera['date']
                    hora_carrera = carrera['time']


                    
                    mensaje_respuesta += f"Carrera Nº: {round} \n\n Nombre: {nombre_carrera}\n Circuito: {circuito}\n\n Horarios: \n\n Libres 1: \n\n🗓️ {fecha_entrenamientos1} \n⏰ {hora_entrenamientos1}\n\nLibres 2: \n\n🗓️ {fecha_entrenamientos2}\n⏰ {hora_entrenamientos2}\n\nLibres 3: \n\n🗓️ {fecha_entrenamientos3}\n⏰ {hora_entrenamientos3}\n\nClasificación: \n\n🗓️ {fecha_clasificacion}\n⏰ {hora_clasificacion}\n\n🏁 Carrera: \n\n🗓️ {fecha_carrera}\n⏰ {hora_carrera}\n\n"

                update.message.reply_text(mensaje_respuesta)
            else:
                update.message.reply_text("No hay próximas carreras programadas para Fernando Alonso en la temporada actual.")

        except Exception as e:
            print(f"Error al procesar la respuesta de la API: {e}")
            update.message.reply_text("Lo siento, no pude obtener la información sobre las próximas carreras de Fernando Alonso en este momento.")
    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')




# ---------- CLASIFICACIÓN ----------

def clasificacion(update: Update, context: CallbackContext)-> None:
    global bot_iniciado

    if bot_iniciado:
        try:
            # OBTIENE LA CLASIFICACIÓN DE PILOTOS
            url_clasificacion = "https://ergast.com/api/f1/current/driverStandings.json"
            response_clasificacion = requests.get(url_clasificacion).json()

            # FILTRA LA CLASIFICACIÓN PARA ENCONTRAR A FERNANDO ALONSO
            clasificacion_alonso = next(
                (item for item in response_clasificacion.get('MRData', {}).get('StandingsTable', {}).get('StandingsLists', [{}])[0].get('DriverStandings', [])
                if item.get('Driver', {}).get('driverId') == 'alonso'), None)

            if clasificacion_alonso:
                posicion = clasificacion_alonso.get('position', 'No disponible')
                puntos = clasificacion_alonso.get('points', 'No disponible')
                victorias = clasificacion_alonso.get('wins', 'No disponible')


                update.message.reply_text(f"Ocupo actualmente la {posicion}ª posición en la clasificación de pilotos con {puntos} puntos y {victorias} victorias.")
            else:
                update.message.reply_text("La información de la posición de Fernando Alonso no está disponible en este momento.")


        except requests.exceptions.RequestException as req_error:
            print(f"Error de solicitud al obtener la clasificación de Fernando Alonso: {req_error}")
            return None
        except Exception as e:
            print(f"Error al obtener la clasificación de Fernando Alonso: {e}")
            return None
        
    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')




# ---------- CITAS ----------


# LISTA DE FRASES DE FERNANDO ALONSO
citas_fernando_alonso = [
    "La victoria es la única cosa que importa en la Fórmula 1.",
    "No me importa si la gente en el paddock me llama arrogante. Lo que importa es si ganas en domingo.",
    "En la Fórmula 1, no hay victorias pequeñas.",
    "En la lluvia, siempre hay oportunidades.",
    "La velocidad no viene de la potencia, sino de la confianza.",
    "El rendimiento está relacionado con la felicidad.",
    "Lo importante no es cuánto corres, sino cuánto disfrutas corriendo.",
    "Cuando conduzco, estoy en mi propio mundo."]

def obtener_cita_fernando_alonso(update: Update, context: CallbackContext):
    global bot_iniciado

    if bot_iniciado:
        # SELECCIONA ALEATORIAMENTE UNA FRASE DE LA LISTA
        cita_seleccionada = random.choice(citas_fernando_alonso)

        # ENVÍA LA CITA AL USUARIO
        update.message.reply_text(f"Alguna de mis frases son:\n'{cita_seleccionada}'")

    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')


# ---------- CARRERA EN DIRECTO ----------

def carrera_en_vivo(update: Update, context: CallbackContext) -> None:
    global bot_iniciado

    if bot_iniciado:

        movistar= "https://ver.movistarplus.es"
        DAZN = "https://www.dazn.com"
        F1TV = "https://f1tv.formula1.com/"

        # MENSAJE CON LOS ENLACES
        mensaje_respuesta = f"Aquí te dejo los enlaces para seguir la próxima carrera de Fórmula 1:\n\n"
        mensaje_respuesta += f"Television: \n\n Movistar: {movistar} \n DAZN: {DAZN} \n F1TV: {F1TV}"

        update.message.reply_text(mensaje_respuesta)

    else:
        update.message.reply_text('Por favor, debes iniciar primero el bot con /startbot.')


# ---------- AYUDA ----------

def ayuda(update: Update, context: CallbackContext) -> None:
    comandos = [
        "/startbot - Inicia el Bot",
        "/saludo - Manda un saludo al chat",
        "/mensaje - Manda un mensaje al chat",
        "/ultima_carrera - Muestra información  de la última carrera",
        "/proximas_carreras - Muestra información sobre las próximas carreras",
        "/clasificacion - Muestra la clasificación actual",
        "/citas - Muestra algunas frases de Alonso",
        "/carrera - Actualiza la carrera en directo",
        "/help - Muestra los comandos que se pueden mandar",
        "/finish - Termina la conexión con el Bot"]
    
    update.message.reply_text("\n".join(comandos))


# ---------- FINALIZAR BOT ----------

def finalizar_bot(update: Update, context: CallbackContext) -> None:
    global bot_iniciado
    bot_iniciado = False
    update.message.reply_text('Bot finalizado. Para iniciar de nuevo, utiliza /startbot.')



# ---------- MAIN ----------

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    # MANEJADOR DEL COMANDO /saludo
    dp.add_handler(CommandHandler("saludo", saludo))

    # MANEJADOR DEL COMANDO /startbot
    dp.add_handler(CommandHandler("startbot", iniciar_bot))

    # MANEJADOR DEL COMANDO /help
    dp.add_handler(CommandHandler("help", ayuda))

    # MANEJADOR DEL COMANDO /finish
    dp.add_handler(CommandHandler("finish", finalizar_bot))

    # MANEJADOR DEL COMANDO /mensaje
    dp.add_handler(CommandHandler("mensaje", generar_mensaje))

    # Manejar mensajes normales en el grupo
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, saludar_usuario))

    # Manejar nuevos miembros
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, on_new_member))

    # MANEJADOR DEL COMANDO /citas
    dp.add_handler(CommandHandler("ultima_carrera", ultima_carrera))

    # MANEJADOR DEL COMANDO /proximas_carreras
    dp.add_handler(CommandHandler("proximas_carreras", proximas_carreras))

    # MANEJADOR DEL COMANDO /clasificacion
    dp.add_handler(CommandHandler("clasificacion", clasificacion))

    # MANEJADOR DEL COMANDO /citas
    dp.add_handler(CommandHandler("citas", obtener_cita_fernando_alonso))

    # MANEJADOR DEL COMANDO /carrera
    dp.add_handler(CommandHandler("carrera", carrera_en_vivo))

    # INICIA EL BOT
    updater.start_polling()

    # MANTIENE EJECUTANDOSE EL BOT HASTA QUE SE PRESIONE Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()