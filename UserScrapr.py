from selenium import webdriver
import numpy as np
import PinterestScrapper

def main():
	# crear el driver
	driver = webdriver.Chrome()
	driver.implicitly_wait(4)
	# credenciales:
	email = "jimbokoln@gmail.com"
	passw = "zinzuk-pohjeh-6qagnE"
	# lista de usuarios
	users, sex, age = np.genfromtxt('user_list.txt', unpack=True, dtype=None, encoding=None)
	# crear el PinterestScrapper
	ps = PinterestScrapper.PinterestScrapper(users[12:], driver, email, passw)
	# Empezar a obtener la info de los usuarios
	ps.scrapUsers()

if __name__ == '__main__':
	main()