# ChatGPTerminal

git clone https://github.com/cubanoar/ChatGPTerminal.git

cd ChatGPT

pip install -r requirements.txt

En el archivo config.py estan las variables USER = "TU_USARIO_DE_CHATGPT"
PASS = "TU_PASSWORD_DE_CHATGPT" en las mismas debes introducir tus credenciales para el login

Si queremos ejecutarlo sin que se abra el navegador debemos modificar la linea 29 de chatgpt.py
    
    self.driver = iniciar_webdriver(headless='new', pos="izquierda")

Con headless=False se abre el navegador a la izquierda de la pantalla

python chatgpt.py