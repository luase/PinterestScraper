from selenium import webdriver
import PinterestScrapper

def main():
	# crear el driver
	driver = webdriver.Chrome()
	driver.implicitly_wait(4)
	# lista de usuarios
	users = ["jasajsas", "pamemimsnnoabre"]
	# crear el PinterestScrapper
	ps = PinterestScrapper.PinterestScrapper(users, driver)
	# Empezar a obtener la info de los usuarios
	ps.scrapUsers()

if __name__ == '__main__':
	main()