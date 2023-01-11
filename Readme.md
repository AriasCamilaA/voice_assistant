# Lexi - Asistente e Voz
## Manual de Usuario
© Camila Alexandra Arias Ruiz

**Índice**
1. Instalación
2. Modo de Uso

Lexi es un asistente que funciona a través de comandos de voz.

### 1. Instalación 
Descargar el repositorio y extraerlo, o clonar el repositorio en la carpeta deseada
```bash
 git init
 git clone https://github.com/AriasCamilaA/voice_assistant
```
Una vez desacargado, ejecutar la terminal en la dirección donde se descargo el repositorio. Crear entorno virtual y descargar los requerimientos.
```bash
 py -m venv env
 cd .\env\Scripts\
 .\activate
 cd ..\..
 pip install -r requirements.txt
```
Ejecutar el asistente de voz
```
 py .\main.py
```
### 2. Modo de Uso

Hacer click en iniciar

![image](https://user-images.githubusercontent.com/115506864/206819897-0c040d98-c279-4be7-bc46-aa316f52e39e.png)

El asistente empezará a hablar y el usuario deberá decir la orden cuándo diga `>> Escuchando...`

![image](https://user-images.githubusercontent.com/115506864/206820626-a6a5cbb0-3bed-4e1b-b2a9-3b192237cfc2.png)

Ejemplo di: "Lexi qué hora es" y ella te respondera con su voz y mostrara en pantalla el resultado

![image](https://user-images.githubusercontent.com/115506864/206820491-7ac9e041-73de-46c6-8904-03b608154927.png)

Tiene la opción de utilizar estas funcionalidades: 
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
    
 Para salir del asistente di 'Lexi salir del asistente' o 'Adiós" y así se cerrara el programa.

