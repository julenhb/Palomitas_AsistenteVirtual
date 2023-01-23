import os
import subprocess

import speech_recognition as sr
import pyttsx3
import pywhatkit as pywhat
import tweepy
import datetime
import random
import webbrowser as web

# Variables
name = 'palomitas'

#Claves para twitter:
CUSTOMER_KEY = "pU2O3q6lmLiPBoqeFBviS54Cy"
CUSTOMER_SECRET= "9B747TRvA70CVkXsiLtioiR8DebDYizNqnLV60AiunFsFxrbHp"
ACCESS_TOKEN = "389681462-n6MN4k94hLTYQiaPxEIxKhIB4CorFUyX5BLaCTz6"
ACCESS_TOKEN_SECRET = "vpGMx6Ob0u1F76wWxlVgdNOqD4TWcky7PeCyPP5KxSU7K"

auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#MÉTODO PARA BÚSQUEDA AVANZADA DE TUITS
def buscarTuit():
    talk("¿Qué palabra quieres buscar?")
    keyword = listen()
    talk("Cuántos tuits quieres buscar?")
    cantidad = int(listen())

    #Con el siguiente bucle se buscan tweets a través de la palabra clave que dijimos, y busca la cantidad que digamos
    for tweet in tweepy.Cursor(api.search_tweets, lang='es', q=keyword).items(cantidad):
        talk("El tweet dice " + tweet.text)
        talk("Fue creado a " + str(tweet.created_at))
        talk("Número de favoritos " + str(tweet.favorite_count))
        talk("Número de retweets " + str(tweet.retweet_count))
        talk("Coordenadas del tuit " + str(tweet.tweet_coordinates))

def tuitear(texto):
    api.update_status(texto)


# Hacemos un listener para el reconocimiento de la voz
listener = sr.Recognizer()

# Comandos de SALIDA de voz
engine = pyttsx3.init()

# Voces
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

"""
for voice in voices:
    print(voice)
#CON ESTE BUCLE PODEMOS VER CUÁNTAS VOCES PODEMOS USAR
"""

archivos = {

}
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Comandos de ENTRADA de voz
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
                print(rec)
    except:
        pass
    return rec

#método para escribir en un archivo
def write(f):
    talk("¿Qué quieres que escriba")
    text = listen()
    #Nos escucha y se lo pasamos al método de escritura, os.linesep sirve para escribir en líneas separadas
    f.write(text + os.linesep)
    talk("Terminé, mira qué bien me ha quedado")
    #Abrimos el archivo
    subprocess.Popen("nota.txt", shell=True)


"""Se intentó
def chiste():
    contador = random.randint(0, 2)
    broma = ''
    match contador:
        case '0':
            broma = "Programar odú es la cosa más divertida que se ha hecho jamás en la historia"
        case '1':
            broma = "Camarero, ¿tiene alitas? Claro que sí. Pues tráigame una cerveza volando."
        case '2':
            broma = "Buenas, venía a sacarme el carnet de conducir. ¡Pero si esto es el hospital! Ya, es que se me ha metido por el culo"

    return broma"""




def run():

    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Ahí va un temazo, ' + music)
        pywhat.playonyt(music)
        SystemExit

    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%H:%M')
        talk('Son las ' + hora)
        talk('¿Necesitas algo más Yulen?')
        run()

    elif 'busca' in rec:
        search = rec.replace('busca', '')
        web.open_new_tab("https://www.google.com/search?q=" + search)
        talk('He encontrado esto en google')
        SystemExit

    elif 'joke' in rec:
        #res = chiste()
        talk("Buenas, venía a sacarme el carnet de conducir. ¡Pero si esto es el hospital! Ya, es que se me ha metido por el culo")
        talk("¿Quieres escuchar otro?")
        otro = listen()
        if 'yes' in otro:
            talk("Vale, este es bueno")
            talk("Programar odú es la cosa más divertida que se ha hecho jamás en la historia")
            talk("¿Quieres escuchar otro?")
            otro2 = listen()
            if 'yes' or 'another' in otro2:
                talk("Venga va, el último")
                talk("¿Cuál es el pez más lento del mundo? El delfín, porque siempre está al final")
                talk("¿Y el más rápido? Pues el pezón, porque va echando leches")
                talk("¿Quieres escuchar otro?")
                otro3 = listen()
                if 'yes' or 'another' in otro3:
                    talk("Yulen, estás muy solo, deberías salir a la calle, hacer amigos, esas cosas.")
                    talk("¿Algo más?")
                    choose = listen()
                    if 'goodbye' in choose:
                        talk("De acuerdo, hasta la próxima, Yulen")
                        SystemExit
            else:
                talk("De acuerdo, ¿Algo más?")
                run()
        else:
            talk("De acuerdo, ¿Algo más?")
            run()

    elif 'beautiful' in rec:
        talk("La persona más bella de esta clase es Yulen, sin ninguna duda")
        talk("De hecho, nadie me está amenazando con borrar la carpeta System32 si digo lo contrario")
        talk('¿Necesitas algo más Yulen?')
        run()

    elif 'escribe' in rec:
        try:
            with open("nota.txt", 'a') as f: #si el archivo ya existe, la a nos dice que lo abriremos en modo de sobreescritura
                write(f)
        except FileNotFoundError as e:
            file = open("nota.txt", 'w') #la w indica que lo abrimos en modo escritura por primera vez (es decir, lo crea)
            write(file)

    elif 'send' in rec:
        talk("¿Qué quieres que tuitee?")
        tuit = listen()
        tuitear(tuit)

    elif 'encuentra' in rec:
        buscarTuit()

    elif 'adios' in rec:
        talk("No es un adiós, es un hasta luego")
        SystemExit

    else:
        talk("Lo siento, no te he entendido, vuelve a intentarlo")
        run()

talk("Hola Yulen, ¿qué necesitas?")
run()


