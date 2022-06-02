#--------------------------------------Importamos librerias--------------------------------------------
from tkinter import *
#LIBRERIA PARA ENVIAR CORREOS
import smtplib
#LIBRERIA RECONOCIMIENTO DE VOZ
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import pywhatkit as rep
from gtts import gTTS
import webbrowser
import speech_recognition as sr
import time
from playsound import playsound
import mediapipe as mp 
import math
#from EMOTION_FACE import *

#################################### EMOTION_FACE  #################################################3333
feliz=0
triste=0
enojado=0
asombrado=0
#____________________Realizamos lavideocaptura_____________
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#___________________Creamos nuestra función de dibujo____________________
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

#__-------creamos un objeto donde almacenaremos la malla facial______-
mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

#________________definimos la función para reconocimiento de emociones_____________

def Emotion():
    #global emocion

#_____________________Creamos el while principal___________________________

    while True:
        ret,frame = cap.read()
        #__--Correción de color_____________
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #observamos resultados___________________________
        resultados = MallaFacial.process(frameRGB)

    #___________Creamos unas listas donde almacenaremos los resultados_______-
        px = []
        py = []
        lista = []
        r = 5 
        r = 3 

        if resultados.multi_face_landmarks:
            for rostros in resultados.multi_face_landmarks:
                mpDibujo.draw_landmarks(frame, rostros,mpMallaFacial.FACEMESH_CONTOURS, ConfDibu, ConfDibu)

                for id,puntos in enumerate(rostros.landmark):
                    al, an, c = frame.shape
                    x,y = int(puntos.x*an), int(puntos.y*al)
                    px.append(x)
                    py.append(y)
                    lista.append([id,x,y])
                    if len(lista)==468:
                        #ceja derecha
                        x1, y1 = lista[65][1:]
                        x2, y2 = lista[158][1:]
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        longitud1 = math.hypot(x2 - x1, y2 - y1)

                        #ceja izquierda
                        x3, y3 = lista[295][1:]
                        x4, y4 = lista[385][1:]
                        cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                        longitud2 = math.hypot(x4 -x3, y4 - y3)
                        #boca extremos
                        x5, y5 = lista[78][1:]
                        x6 ,y6 = lista[308][1:]
                        cx3, cy3 = (x5 +x6) // 2, (y5 + y6) // 2
                        longitud3 = math.hypot(x6 -x5, y6 - y5)

                        #boca apertura
                        x7, y7 = lista[13][1:]
                        x8 ,y8 = lista[14][1:]
                        cx4, cy4 = (x7 +x8) // 2, (y7 + y8) // 2
                        longitud4 = math.hypot(x8 -x7, y8 - y7)


                        #clasificación
                        #bravo
                        if longitud1 < 19 and longitud2 < 19 and longitud3 > 80 and longitud3 < 95 and longitud4 < 5:
                            cv2.putText(frame, 'persona enojada', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            emocion='persona enojada'
                            EMOCION(emocion)
                            #return emocion  
                        #feliz
                        elif longitud1 >20 and longitud1 < 30 and longitud2 > 20 and longitud2 < 30 and longitud3 > 109 and longitud4 > 10 and longitud4 < 20:
                            cv2.putText(frame, 'persona Feliz', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                            emocion='persona feliz'
                            EMOCION(emocion)
                            #return emocion
                        
                        #asombrada
                        elif longitud1 >35 and longitud2 > 35 and longitud3 > 80 and longitud3 < 90 and longitud4 > 20:
                            cv2.putText(frame, 'persona Asombrada', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            emocion = 'persona asombrada'
                            EMOCION(emocion)
                            #return emocion
                        #triste
                        elif longitud1 >20 and longitud1 < 30 and longitud2 > 20 and longitud2 < 35 and longitud3 > 80 and longitud3 < 95 and longitud4 < 5:
                            cv2.putText(frame, 'persona Triste', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0 , 0), 3)
                            emocion = 'persona triste'
                            EMOCION(emocion)
                            #return emocion
            
            cv2.imshow("reconocimiento de emociones ", frame)
            t = cv2.waitKey(1)
            if t == 27:
                break
    cap.release()
    cv2.destroyAllWindows()
    return emocion
def SALIR(emocion):
        #print(contar)
    if feliz==30 or enojado==30 or triste==30 or asombrado==30:
        musica(emocion)
def EMOCION(emocion):
    global feliz
    global triste
    global asombrado
    global enojado
    
    if emocion=='persona triste':
        #print('estas triste')
        triste=triste+1
        SALIR(emocion)
    elif emocion=='persona feliz':
        #print('estas triste')
        feliz=feliz+1
        SALIR(emocion)
    elif emocion=='persona enojada':
        #print('estas triste')
        enojado=enojado+1
        SALIR(emocion)
    elif emocion=='persona asombrada':
        #print('estas triste')
        asombrado=asombrado+1
        SALIR(emocion)



#------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------
'''
def enviar_correo():
        #afiliado = Afiliado()
        # funcion para enviar correos
        #message = f'Hola {datos[0].strip()} {datos[1].strip()} tu EPS saludUN te informa que la fecha programada para tu vacunacion es el {fecha} a las {hora}, recuerda llegar 30 minutos antes.'
        message='mensaje'
        subject = 'asunto'
        message = 'Subject: {}\n\n{}'.format(subject, message)
        
        # Genera la instancia
        try:
            #server = smtplib.SMTP('smtp.gmail.com', 465)
            server = smtplib.SMTP('smtp.live.com', 25)
            # Llama al protocolo ttls
            server.starttls()

            # ingresa al correo de donde enviara el correo
            #server.login('petter5856a@gmail.com', '2001parada')
            server.login('EPSsaludUN@hotmail.com', 'programacionPOO2021')
           
            # envia el correo
            #server.sendmail('EPSsaludUN@hotmail.com', datos[2], message)
            server.sendmail('EPSsaludUN@hotmail.com', datos[2], message)
            print('Citaciones enviadas con éxito')
        except:
            print('no se pudo enviar el correo a ' + 'CREAR VARIABLE NOMBRE')
        # cierra el servidor
        server.quit()
'''
def registrar_usuario():
    usuario_info = usuario.get() #Obetnemos la informacion alamcenada en usuario
    contra_info = contra.get() #Obtenemos la informacion almacenada en contra

    archivo = open(usuario_info, "w") #Abriremos la informacion en modo escritura
    archivo.write(usuario_info + "\n")   #escribimos la info
    archivo.write(contra_info)
    archivo.close()

    #Limpiaremos los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    #Ahora le diremos al usuario que su registro ha sido exitoso
    Label(pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()
    

#--------------------------- Funcion para almacenar el registro facial --------------------------------------
    
def registro_facial():
    #Vamos a capturar el rostro
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Registro Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   #Limpiamos los text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).pack()

    #----------------- Detectamos el rostro y exportamos los pixeles --------------------------
    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)   
    
#------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro():
    global usuario
    global contra  #Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")  #Asignamos el tamaño de la ventana
    
    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text = "Registro facial: debe de asignar un usuario:").pack()
    #Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla1, text = "Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla1, text = "Usuario * ").pack()  #Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack()  #Mostramos en la pantalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra) #Creamos un text variable para que el usuario ingrese la contra
    contra_entrada.pack()
    Label(pantalla1, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla1, text = "Registro Tradicional", width = 15, height = 1, command = registrar_usuario).pack()  #Creamos el boton

    #------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla1, text = "").pack()
    Button(pantalla1, text = "Registro Facial", width = 15, height = 1, command = registro_facial).pack()

#------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------

#___________________________________________FUNCIÓN DE MÚSICA_________________________________  

def musica(emocion):
    #usuario= va dentro de musica como argumento 
    #mensaje = "Welcome to the virtual comfort room. What song do you want to hear?"
    #nombre = "BIENVENIDA.mp3"
    #playsound(nombre)
    
    
    if emocion=='persona triste':
            mens='Parece que tu día no ha sido bueno'
            reproducir_mensajes(mens)
            time.sleep(1)
    elif emocion=='persona feliz':
            mens='Parece que has tenido un gran día'
            reproducir_mensajes(mens)
            time.sleep(1)
    elif emocion=='persona enojada':
            mens='Pareces estar de mal humor'
            reproducir_mensajes(mens)
            time.sleep(1)
    elif emocion=='persona asombrada':
            mens='Parece ser que algo te a sorprendido'
            reproducir_mensajes(mens)
            time.sleep(1)         
    
    mensaje ="bienvenido a la sala de confort virtual. ¿Qué canción quieres escuchar?"
    lenguaje = 'es-us'
    speech = gTTS(text = mensaje, lang = lenguaje, slow = False)
    speech.save("mensaje.mp3")
    os.system("start mensaje.mp3")
    time.sleep(8)
    voz()






def reproducir_mensajes(mensaje1):
    #print("esto es mensaje 1 : " + mensaje1)

    
    mensaje = ("Has dicho" + mensaje1) 
    lenguaje = 'es-us'
    if mensaje1=="no te he entendido":
        mensaje=mensaje1
    elif mensaje1 =="Repite el nombre de la canción, de nuevo por favor":
        mensaje=mensaje1
    elif mensaje1=="repítelo de nuevo por favor":
        mensaje=mensaje1
    elif mensaje1=="hubo un error vuelve a intentar":
            mensaje=mensaje1
    elif mensaje1=='Parece que tu día no ha sido bueno':
            mensaje=mensaje1
    elif mensaje1=='Parece que has tenido un gran día':
            mensaje=mensaje1
    elif mensaje1=='Pareces estar de mal humor':
            mensaje=mensaje1
    elif mensaje1=='Parece ser que algo te a sorprendido':
            mensaje=mensaje1
    speech = gTTS(text = mensaje, lang = lenguaje, slow = False)
    speech.save("mensaje.mp3")
    os.system("start mensaje.mp3")
    time.sleep(3)
    #return mensaje1

def confirmacion(texto):
    print("entro a confirmación")
    r= sr.Recognizer()
    with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                        text = r.recognize_google(audio) 
                        if text == "yes":
                            print("entro al if yes")
                            rep.playonyt(texto)
                            print("SALIR DEL PROGRAMA")
                            exit()
                        if text=="not":
                            print("entro al if not")
                            reproducir_mensajes("Repite el nombre de la canción, de nuevo por favor")
                            #time.sleep(2)
                            voz()
                        else:
                            print("entro al else de confirmacion")
                            print(text)
                            reproducir_mensajes("repítelo de nuevo por favor")
                            time.sleep(2)
                            confirmacion(texto)
                        

                except:
                        print("entro al error")
                        reproducir_mensajes("no te he entendido")
                        confirmacion(texto)
repetir=0                       
def voz():
    global repetir
    if repetir==1:
        repetir=0
        reproducir_mensajes("Repite el nombre de la canción, de nuevo por favor")

    print("entro a voz")
    r= sr.Recognizer()
    with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            #time.sleep(2)
            print("grabando")
            audio = r.listen(source)
            try:
                    
                    text = r.recognize_google(audio)
                    print(text)
                    '''text = recognize_sphinx(audio)
                    #text = r.recognize_google_cloud(audio)
                    #text = recognize_bing(audio)'''
                    if (len(text))!=0:
                        reproducir_mensajes(text)
                        confirmacion(text)
                    else:
                        reproducir_mensajes("no te he entendido")
                        repetir=+1
                        time.sleep(2)
                        voz()
                        
                                         
            except:

                    reproducir_mensajes("hubo un error vuelve a intentar")
                    repetir=+1
                    time.sleep(2)
                    voz()
        



def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
        archivo2 = open(log_usuario, "r")  #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
    
#--------------------------Funcion para el Login Facial --------------------------------------------------------
def login_facial():
#------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Login Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_login = verificacion_usuario.get()    #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)   #Limpiamos los text variables
    contra_entrada2.delete(0, END)

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    
    im_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if usuario_login+".jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.9:
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
            time.sleep(2)
            #musica(usuario_login)
            Emotion()
            #musica()
        if similitud < 0.91:
            print("Rostro incorrecto, Verifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
            
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
            

#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("500x400")   #Creamos la ventana
    Label(pantalla2, text = "Login facial: debe de asignar un usuario:").pack()
    Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla2, text = "").pack()  #Dejamos un poco de espacio
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    verificacion_correo = StringVar()
    #---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text = "Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text = "Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text = "Email * ").pack()
    correo = Entry(pantalla2,textvariable = verificacion_correo)
    correo.pack()
    print(correo)
    #Label(pantalla2, text = "").pack()
    #Button(pantalla2, text = "Inicio de Sesion Tradicional", width = 20, height = 1, command = verificacion_login).pack()

    #------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "").pack()
    Button(pantalla2, text = "Inicio de Sesion Facial", width = 20, height = 1, command = login_facial).pack()
        
#------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("600x600")  #Asignamos el tamaño de la ventana 
    pantalla.title("CONFORD VIRTUAL")       #Asignamos el titulo de la pantalla
    Label(text = "Login Inteligente", bg = "gray", width = "300", height = "2", font = ("Verdana", 13)).pack() #Asignamos caracteristicas de la ventana
    
#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "").pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", height = "2", width = "30", command = login).pack()
    Label(text = "").pack() #Creamos el espacio entre el primer boton y el segundo boton
    Button(text = "Registro", height = "2", width = "30", command = registro).pack()

    pantalla.mainloop()

pantalla_principal()
  
#lista = sr.Microphone.list_microphone_names()
#print(lista)
#musica()





