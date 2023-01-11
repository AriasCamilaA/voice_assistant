from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton
from tkinter import PhotoImage, Canvas
from deep_translator import GoogleTranslator
from datetime import datetime
from email.message import EmailMessage
import speech_recognition as sr
import pywhatkit as pwk 
import pyttsx3
import pyjokes
import wikipedia
import webbrowser
import cv2
import threading

app = CTk()

#Tamaño
window_width = 600
window_height = 500
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2)-20)

#Colores
c_fondo = "#242424"
c_fondo_2 = "#472F52"
c_texto = "#BD7ED9"


#Configuraciones ventana
app.title("  Lexi - Tu Asistente Virtual")
app.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
app.resizable(False, False)
app.configure(bg=c_fondo)
logo = PhotoImage(file = "./GUI/voice-search.png")
app.call("wm", "iconphoto", app._w, logo)

#-------------------------
div = CTkFrame(app, corner_radius=10,fg_color = c_fondo_2)
div.pack(padx=20, pady=20)
Titulo = CTkLabel(div, text="Soy Lexi\nTu asistente de voz", font = ("Helvetica",30))#.grid(columnspan = 3, row = 0)
Titulo.pack(padx=20, pady=20)
#---------------------------
gif = './GUI/gif_small.gif'
framesNum = 28 # Numero de frames que tiene el gif, si no lo conoces ir haciendo tentativos.
frames = [PhotoImage(file=gif, format='gif -index %i' %(i)) for i in range(framesNum)]

def animar(ind):
    """ Actualiza la imagen gif """
    frame = frames[ind]
    ind += 1
    if ind == framesNum:
        ind = 0
    canvas.delete("all")
    canvas.create_image(80.5,87.5,image=frame,anchor="center")
    app.after(18, animar, ind) # Numero que regula la velocidad del gif

canvas = Canvas(bg=c_fondo, highlightbackground=c_fondo, width=150, height=150) # Modificar segun el tamaño de la imagen

canvas.pack(anchor="center")
app.after(0, animar, 0)

div2 = CTkFrame(app, fg_color = c_fondo, width=440)
div2.pack(padx=20, pady=20)

impresion = CTkLabel(div2, text="", font = ("consolas",15),text_color=c_texto)
impresion.pack(padx=20, pady=20)

#----------------------------------------------------
def modificar(mit:str):
    impresion.configure(text=mit)
#-------------------------------------------------------------------------------------

# Configuraciones
now = datetime.now() # Para la hora y fecha actual
listener = sr.Recognizer() # Para el reconocimiento de voz
engine = pyttsx3.init() # Para leer texto
wikipedia.set_lang("es") # Para utilizar el API de Wikipedia en español
traductor = GoogleTranslator(source='es', target='en') # Para utilizar el traductor de español a inglés

#Correo
MAIL_USER = ""
MAIL_PASSWORD = ""
DESTINATARIO = MAIL_USER

FUNCIONALIDADES="""Funciones:
    Puedes decir lexi ....
    'Reproducir _canción o video_' : Para reproducir en youtube
    'Envia un mensaje' o 'Enviar mensaje' : Para ennviar un correo electrónico
    'Di un chiste' : Para decir un chiste al azar
    'Buscar en google _busqueda_' : Para buscar algo en Google
    'Qué hora es' : Para saber la hora actual
    'Qué día es hoy' : Para saber la fecha actual
    'Busca en wikipedia _busqueda_" : Para que nos lea el primer resultado de Wikipedia
    'Tradúceme _texto_" : Para traducir de español a inglés
    'Abre _pagina web_' : Para abrir la página en el navegador (ej: Google, Python, Whatsapp, Netflix, etc )
    'Tomar foto' : Para tomar una foto y almacenarla
    'Salir del asistente' o 'Adiós" : Para salir del asistente
"""
name = "lexi "
bienvenida = "Hola, soy tu asistente de voz, bienvenido"
despedida = "Adiós, Gracias por utilizar este asistente de voz"
opciones = "¿Qué deseas hacer?"
invalido = "No es valido, vuelvelo a decir"

def validar (_text:str):
    """Decide que función ejecutar dependiendo el texto que se le pase por argumento
    """
    text = _text.lower()

    #Limpiando cádena
    if name in text:
        text =  text.replace(name, "")

    #Validando opciones
    if "reproducir " in text:
        text = text.replace("reproducir ","")
        reproductor(text)
        elegir()
    elif "envía un mensaje" in text or "enviar mensaje" in text:
        enviar_msg()
        elegir()
    elif "di un chiste" in text:
        chiste()
        elegir()
    elif "busca en google " in text:
        text = text.replace("busca en google ","")
        buscar(text)
        elegir()
    elif "qué hora es" in text:
        hora()
        elegir()
    elif "qué día es hoy" in text:
        fecha()
        elegir()
    elif "busca en wikipedia " in text:
        text = text.replace("busca en wikipedia ","")
        wiki(text)
        elegir()
    elif "tradúceme " in text:
        text = text.replace("tradúceme ","")
        traducir(text)
        elegir()
    elif "abre " in text or "abrir" in text:
        text = text.replace("abre ","")
        abrir_pagina(text)
        elegir()
    elif "tomar foto" in text or "tómame una foto" in text:
        foto()
        elegir()
    elif "salir del asistente" in text or "adiós" in text:
        decir(despedida)
        app.after(15, func=app.destroy)
    else:
        decir(invalido)
        elegir()

def decir(texto, voz=0):
    """Dice en voz alta el texto que se le pase por argumento, y lo muestra por consola
    """
    voices = engine.getProperty('voices')
    engine.setProperty("voice",voices[voz].id)
    imprimir = f">> {texto}"
    # print(imprimir)
    impresion.after(10,modificar(imprimir))
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    """Escucha lo que diga el usuario por el micrófono
    Returns:
        str: Aquello que escuchó
    """
    with sr.Microphone() as source:
        # print(">> Escuchando...")
        impresion.after(10,modificar(">> Escuchando..."))
        audio = listener.listen(source,10,3)
        try:
            text = listener.recognize_google(audio,language="es-ES")
            # print(f">> Dijiste: {text}")
            return text
        except:
            decir("No pude entenderle, por favor repitalo")
            text = escuchar()
            return text

saludo = 0
def elegir():
    """Permite el funcionamiento del asistente de voz
    """
    global saludo
    if saludo==0:
        saludo +=1
        decir(bienvenida)
    decir(opciones)
    validar(escuchar())

def reproductor(text:str): 
    """Reproduce el video o canción que diga el usuario
    """
    decir(f"Reproduciendo {text}")
    pwk.playonyt(text)

def enviar_msg():
    """enviar un mensaje de correo electrónico
    """
    decir("Por el momento el sistema no te permite enviar correos electrónicos por temas de autenticación")

    # decir("¿Qué mensaje desea enviar?")
    # mensaje = escuchar()
    # decir("¿Qué asunto quiere ponerle?")
    # asunto = escuchar()

    # server = smtplib.SMTP('smtp.gmail.com',587)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(MAIL_USER,MAIL_PASSWORD)
    # server.sendmail(MAIL_USER,DESTINATARIO,mensaje)
    # decir("En un minuto se enviará su mensaje")
    # server.quit()
    # decir("Correo enviafo exitosamente")

def chiste():
    """Dice un chiste al azar
    """
    decir(pyjokes.get_joke("es"))

def buscar(query:str):
    """Busca en Google lo que dice el usuario
    """
    pwk.search(query)
    decir(f"Buscando...{query}")
    decir("Resultados encontrados")

def hora():
    """Dice la hora actual en Colombia
    """
    hora_actual = now.time().strftime('%I:%M:%S %p')
    decir(f"La hora actual es: {hora_actual}")

def fecha():
    """Dice la fecha actual en colombia
    """
    traductorEn = GoogleTranslator(source='en', target='es')
    fecha_actual = now.strftime('%A, %d de %B de %Y')
    decir(f"Hoy es: {traductorEn.translate(fecha_actual)}")

def wiki(query):
    """Lee el resultado de una busqueda en Wikipedia
    """
    try:
        text = wikipedia.summary(query, sentences = 1 , chars = 0 , auto_suggest = True , redirect = True )
    except:
        text = "No encontre resultados"
    decir(text)

def abrir_pagina(text):
    """Abrir una nueva pagina en el navegador
    """
    paginas = {
        "google" : "https://www.google.com/?hl=es",
        "python" : "http://www.python.org",
        "whatsapp" : "https://web.whatsapp.com/",
        "teams" : "https://www.microsoft.com/es-co/microsoft-teams/log-in",
        "twitter" : "https://twitter.com/?lang=es",
        "instagram" : "https://www.instagram.com/",
        "canva" : "https://www.canva.com/",
        "netflix" : "https://www.netflix.com/co/",
        "tiktok" : "https://www.tiktok.com/es/"
    }

    if paginas.get(text,"NO") != "NO":
        decir(f"Abriendo {text}")
        webbrowser.open(paginas[text], new=2, autoraise=True)
    else:
        decir("No pude abrir la página, intenta con otra")

def foto():
    """tomar una foto
    """
    decir("Tomando foto")
    cap = cv2.VideoCapture(0)

    leido, frame = cap.read()

    if leido == True:
        foto = "foto.png"
        cv2.imwrite(foto, frame)
        decir("Foto tomada correctamente")
    else:
        decir("Error al acceder a la cámara")
    cap.release()

def traducir(text):
    """Traduce del inglés al español"""
    traducido = traductor.translate(text)
    decir(traducido, voz=1)

def mi_asistente():
    # app.mainloop()
    print(FUNCIONALIDADES)
    decir(bienvenida)
    elegir()

seleccionar = threading.Thread(target=elegir)

def iniciar():
    print(FUNCIONALIDADES)
    boton.configure(state= "disabled")
    seleccionar.start()

boton = CTkButton(app,text="Iniciar",command=iniciar, fg_color=c_fondo_2, hover_color="#761CE6")
boton.pack()


app.mainloop()
#--------------------------------------------------

def main():
    print("---Asistente de voz----")

if __name__ == "__main__":
    main()
