#modulos de python
import os
import sys
import time
import pickle
import tempfile

#modulos de terceros
from selenium.webdriver.common.by import By #para buscar por tipo de elemento 
from selenium.webdriver.support.ui import WebDriverWait #para esperar por elementos en selenium 
from selenium.webdriver.support import expected_conditions as ec #para condiciones en selenium
from selenium.webdriver.common.keys import Keys #para pulsar teclas especiales (ej: AvPag, ENTER)

#modulos propios
from config import *
from colores import *
from helpers import cursor_arriba
from iniciar_webdriver_uc import iniciar_webdriver

#Ahora nos mandamos una clase
class ChatGpt:
    #constructor
    def __init__(self, username, password):
        """Iniciamos webdriver y nos logeamos en CHatGpt"""
        self.USER = username
        self.PASS = password
        self.COOKIES_FILE = f'{tempfile.gettempdir()}/openai.cookies'
        print(f'Iniciando WEBDRIVER')
        self.driver = iniciar_webdriver(headless=False, pos="izquierda")
        self.wait = WebDriverWait(self.driver, 30)
        login = self.login_openai()
        print()
        if not login:
            sys.exit(1)


    def login_openai(self):
        """ realiza login en CHatGpt por cookies o desde cero(se guardan las cookies) """

        #LOGIN POR COOKIES
        #si existen las cookies
        if os.path.isfile(self.COOKIES_FILE):
            #obtenemos las cookies
            cookies = pickle.load(open(self.COOKIES_FILE, "rb"))
            #cargamos robots.txt del dominio correspondiente
            print(f'\33[K{magenta}cargando robots..txt{reset}')
            self.driver.get("http://chat.openai.com/robots.txt")
            #añadimos las cookies al navegador
            for cookie in cookies:
                cursor_arriba()
                print(f'\33[K{magenta}cargando cookie: {cookie["name"]}{reset}')
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            cursor_arriba()
            print(f'\33[K{magenta}cargando chatGPT{reset}')
            self.driver.get("http://chat.openai.com/")
            #comprobamos si el login es correcto
            login = self.comprobar_login()
            #si el login es correcto
            if login:
                print(f'\33[K{blue}LOGIN POR COOKIES: {green}{bold}OK{reset}')
                return login
            #si el login ha fallado
            else:
                print(f'\33[K{blue}LOGIN POR COOKIES: {red}{bold}FALLIDO{reset}')

        #LOGIN DESDE CERO
        print(f'\33[K{blue}LOGIN DESDE CERO{reset}')
        print(f'\33[K{magenta}cargando chatGPT{reset}')
        self.driver.get("http://chat.openai.com/")

        #click en login
        cursor_arriba()
        print(f'\33[K{magenta}click en "login"{reset}')
        e = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
        e.click()

        #introducimos el usuario
        cursor_arriba()
        print(f'\33[K{magenta}introduciendo el usuario{reset}')
        e = self.wait.until(ec.element_to_be_clickable((By.ID, "username"))) 
        e.send_keys(self.USER)

        #click en continue
        cursor_arriba()
        print(f'\33[K{magenta}click en "Continue"{reset}')
        e = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[name='action']"))) 
        e.click()

        #introducimos el password
        cursor_arriba()
        print(f'\33[K{magenta}introduciendo el password{reset}')
        e = self.wait.until(ec.element_to_be_clickable((By.ID, "password"))) 
        e.send_keys(self.PASS)
        
        #click en continue
        cursor_arriba()
        print(f'\33[K{magenta}click en "Continue"{reset}')
        e = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div.c813b1bdc"))) 
        e.click()
        
        #comprobar si el login es correcto
        login = self.comprobar_login()

        #si el login es correcto
        if login:
            #guardamos las cookies
            pickle.dump(self.driver.get_cookies(), open(self.COOKIES_FILE, "wb"))
            print(f'\33[K{blue}LOGIN DESDE CERO: {green}{bold}OK{reset}')
        #si el login ha fallado
        else:
            print(f'\33[K{blue}LOGIN DESDE CERO: {red}{bold}FALLIDO{reset}')
        return login
        


    def comprobar_login(self, tiempo=30):
        """ Devuelve True si estamos logueados y False en caso contrario.
         tiempo: cantidad de segundos mientras las cuales se comprobara si el login es correcto """
        
        login = False
        while tiempo > 0:
            #click en "Next"
            try:
                e = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//div[text()='Next']")))
                e.click()
            except:
                pass
            #click en "Done" CREO NO APARECE MAS
            try:
                e = self.driver.find_element(By.XPATH, "//div[text()='Done']")
                e.click()
            except:
                pass
            #login correcto (click en la caja de texto)
            try:
                e = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "textarea[tabindex='0']")))
                e.click()
                login = True
                break
            except:
                pass
            #login incorrecto
            try:
                e = self.driver.find_element(By.ID, "username")
                break
            except:
                pass
            #sesion expirada
            try:
                e = self.driver.find_element(By.CSS_SELECTOR, "h3.text-lg")
                if "session has expired" in e.text:
                    cursor_arriba()
                    print(f'{yellow}\33[KLA SESION HA EXPIRADO{reset}')
                    print()
                    break
            except:
                pass
            #pausa
            cursor_arriba()
            print(f'{magenta}\33[Kcomprobando login...{tiempo}{reset}')
            time.sleep(0.5)
            tiempo -= 1
        #eliminamos el ultimo print
        cursor_arriba()
        print('\33[K')#eliminamos el contenido de la linea
        cursor_arriba(2)
        return login
    
    def chatear(self, prompt):
        """ Introduce un pront y devuelve el resultado generado por chatGPT. """
        #introducimos el prompt
        e = self.driver.find_element(By.CSS_SELECTOR, "textarea[tabindex='0']")
        e.send_keys(prompt)
        #pulsamos el boton de enviar (el avioncito)
        e = self.driver.find_element(By.CSS_SELECTOR, "button.absolute.p-1")
        e.click()
        # GENERACION DE LA RESPUESTA
        # iniciamos el string de la respuesta
        respuesta = ""
        #timestamp de inicio de la generacion de la respuesta
        inicio = time.time()
        while True:
            #extraemos el texto generado
            e = self.driver.find_elements(By.CSS_SELECTOR, "div.markdown")[-1]
            respuesta = e.text

            # elemento de los 3 puntos animados mientras se genera la respuesta
            puntos = self.driver.find_elements(By.CSS_SELECTOR, "div.text-2xl")

            if len(puntos) == 0:
                break

            #mostramos el tiempo transcurrido
            segundos = int(time.time() - inicio)
            if segundos:
                print(f'\33[K{cyan}generando respuesta...{reset}{segundos}segundos ({len(respuesta)})')
                time.sleep(1)
                cursor_arriba()

        # informamos del tiempo que ha tardado en genrarse la respuesta
        print(f'\33[K{magenta}Respuesta generada en {white}{segundos} {magenta}segundos{reset}')

        #extraemos el texto generado otra vez por si faltaba algo
        e = self.driver.find_elements(By.CSS_SELECTOR, "div.markdown")[-1]
        respuesta = e.text

        return respuesta

        

    def cerrar(self):
        print(f'\33[K{blue}Saliendo...{reset}')
        self.driver.quit()


#MAIN ###################################
if __name__ == '__main__':
    chatgpt = ChatGpt(USER,PASS)
    #limpiar pantalla
    print(f"{cleanScreen}")
    #bucle pricipal
    while True:
        prompt = input(f'{blue}{USER} [S=Salir]: {reset} ')
        #si se opta por terminar
        if prompt.lower() == "s":
            chatgpt.cerrar()
            sys.exit()
        else:
            #enviamos el prompt
            respuesta = chatgpt.chatear(prompt)
            print(f'\33[K{white}{respuesta}{reset} ')
            print()
    