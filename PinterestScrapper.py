import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlretrieve
from selenium.webdriver.support import ui
import os
import re

def saveHTML(driver, file):
    try:
        filename = os.path.join(file, "source.html")
        with open(str(filename), "w") as text_file:
            html = BeautifulSoup(driver.page_source, 'html.parser')
            print(html, file = text_file)
    except:
        pass


# Define un scraper de un pin de Pinterest
class PinScrapper(object):
    def __init__(self, pin, board, driver):
        self.pin    = pin
        self.board  = board
        self.driver = driver

    def pinDir(self):
        self.board = self.board[:-1]
        pin_dir = './data/' + self.board + self.pin[4:]
        if not os.path.exists(pin_dir):
            os.makedirs(pin_dir)

    def downloadImage(self, image):
        try:
            pin_dir  = "./data/" + self.board + self.pin[4:]
            filename = os.path.join(pin_dir, "image.jpg")
            urlretrieve(image, filename)
        except Exception:
            pass

    def downloadText(self, text, name):
        try:
            pin_dir  = "./data/" + self.board + self.pin[4:]
            filename = os.path.join(pin_dir, str(name) + ".txt")
            with open(str(filename), "w") as text_file:
                print(text, file = text_file)
        except:
            pass

    def getPinInfo(self):
        self.driver.get("https://pinterest.com" + str(self.pin))
        time.sleep(2)
        html = BeautifulSoup(self.driver.page_source, "html.parser")
        for mainContainer in html.find_all("div", {"class": "mainContainer"}):
            for pin in mainContainer.find_all("div", {"class": "closeupContainer"}):
                for img in pin.find_all("img"):
                    image = img.get("src")
                    alt   = img.get("alt")
                    if "564" in image:
                        self.downloadImage(image)
                        self.downloadText(alt, 'alt')
                        break
                for h5 in pin.find_all('h5'):
                    for div in h5.find_all('div'):
                        title = div.text 
                        self.downloadText(title, 'title')
                for div in pin.find_all("div", {"class": "_wa _0 _1 _2 _we _3c _d _b _5"}):
                    descr = div.text
                    self.downloadText(descr, 'descr')
        saveHTML(self.driver, "./data/" + self.board + self.pin[4:])

    def scrapPin(self):
        self.pinDir()
        self.getPinInfo()



# Define un scrapper de un board de Pinterest.
class BoardScrapper(object):
    # Inicialización del objeto
    def __init__(self, board, driver):
        self.board_dir = ""
        self.board     = board
        self.driver    = driver
        self.pins      = []

    # Método para crear el directorio donde se va guardar la información
    # del board  
    def boardDir(self):
        self.board_dir = "./data/" + self.board
        if not os.path.exists(self.board_dir):
            os.makedirs(self.board_dir)

    def collectPins(self):
        self.boardDir()
        self.driver.get('https://www.pinterest.com/' + str(self.board))
        start    = time.time()
        run_time = time.time()
        # correr hasta que se tengan max. 1000 pins o pasen 5s de inactividad.
        while len(self.pins) < 10000 and start -  run_time < 5:
            # Reiniciar el temporizador
            start = time.time()
            html  = BeautifulSoup(self.driver.page_source, 'html.parser')
            # encontrar los pins
            for pinWrapper in html.find_all("div", {"class": "pinWrapper"}):
                for a in pinWrapper.find_all("a"):
                    pin = str(a.get("href"))
                    if len(pin) < 40 and pin not in self.pins and "A" not in pin:
                        # nuevo limite de tiempo.
                        run_time = time.time()
                        self.pins.append(pin)                        
            # Scroll down now                
            self.driver.execute_script("window.scrollBy(0,90)")

    # Método para recolectar los links de los pins
    def scrapPins(self):
        self.collectPins()
        saveHTML(self.driver, self.board_dir)
        for pin in self.pins:
            ps = PinScrapper(pin, self.board, self.driver)
            ps.scrapPin()

# Define un scrapper de un usuario de Pinterest.
class UserScrapper(object):
    # Inicialización del objeto
    def __init__(self, username, driver):
        self.user_dir = ""    
        self.username = username
        self.driver   = driver
        self.boards   = []
    
    # Método para crear el directorio donde se va guardar la información
    # del usuario
    def userDir(self):
        self.user_dir = "./data/" + self.username
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def collectBoards(self):
        self.userDir()
        self.driver.get('https://www.pinterest.com/' + str(self.username))
        start    = time.time()
        run_time = time.time()
        # correr hasta que se tengan max. 500 tableros o pasen 5s de inactividad.
        while len(self.boards) < 500 and start - run_time < 10:
            # Reiniciar el temporizador
            start = time.time()
            html  = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Encontrar los tableros
            for boardWrapper in html.find_all('div', {'class': 'zI7 iyn Hsu'}):
                for a in boardWrapper.find_all('a'):
                    board = str(a.get('href'))
                    if self.username in board and board not in self.boards:
                        # Nuevo timelimit.
                        run_time = time.time()
                        self.boards.append(board)
            # Moverse hacia abajo en la página
            self.driver.execute_script('window.scrollBy(0,90)')
        # hay algunos links que no queremos, por ejemplo:
        # https://www.pinterest.com/username/followers
        self.boards = self.boards[5:]

    def scrapBoards(self):
        self.collectBoards()
        # guardamos el html que describe la pagina del usuario.
        saveHTML(self.driver, self.user_dir)
        for board in self.boards:
            bs = BoardScrapper(board, self.driver)
            bs.scrapPins()

# Define un Scrapper para varios usuarios de Pinterest.
class PinterestScrapper(object):
    # Inicialización con parámetros. users debe ser un arreglo de strings
    # con los nombres de usuarios.
    def __init__(self, users, driver, email, passw):
        self.users     = users
        self.driver    = driver
        self.login_url = "https://www.pinterest.com/login/?referrer=home_page"
        self.email     = email
        self.passw     = passw

    # Inicia sesión en Pinterest encontrando los forms, llenándolos y
    # enviando.
    def login(self):
        self.driver.get(self.login_url)
        email = self.driver.find_element_by_xpath("//input[@type='email']")
        passw = self.driver.find_element_by_xpath("//input[@type='password']")
        email.send_keys(self.email)
        passw.send_keys(self.passw)
        passw.submit()
        time.sleep(5)

    # Método del objeto para obtener la información de los usuarios en
    # la lista.
    def scrapUsers(self):
        self.login()
        for user in self.users:
            us = UserScrapper(user, self.driver)
            us.scrapBoards()