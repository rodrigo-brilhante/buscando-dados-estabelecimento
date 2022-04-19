import json
from logging import exception
from random import randint
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import sys

class Google():
	def getTitulo(self, driver):
		try:
			return driver.find_element(By.XPATH, '//*[@id="gsr"]/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[1]/div[1]/div[1]/div[1]').text.strip()
		except Exception as ex:
			print("*****************************************\n",ex)
			return ''

	def getNota(self, driver):
		try:
			return driver.find_element(By.XPATH, '//*[@id="gsr"]/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[1]/div[3]/div[1]/span').text.strip()
		except Exception as ex:
			print("*****************************************\n",ex)
			return ''

	def getNumeroAvaliacao(self, driver):
		try:
			return driver.find_element(By.XPATH, '//*[@id="gsr"]/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[1]/div[3]/div[1]/div/span/span').text.strip()
		except Exception as ex:
			print("*****************************************\n",ex)
			return ''

	def getEndereco(self, driver):
		try:
			return driver.find_element(By.XPATH, '//*[@id="gsr"]/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[1]/div[1]/div[1]/div[2]').text.strip()
			# html = BeautifulSoup(driver.page_source, 'html.parser')
			# spans = html.find_all('spans')

			# for span in spans:
			# 	if "Endereço" in span.text:
			# 		return span.find_next('span').text.strip()
		except Exception as ex:
			print("*\n",ex)
			return ''

	def filter(self, array, key, value):
			keyValList = [value]
			expectedResult = [d for d in array if d[key] in keyValList]
			return len(expectedResult) > 0

	def get(self, nomeEmpresa, qtdReview):
		print('google')
		chrome_options = Options()
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument('--kiosk-printing')
		# chrome_options.add_argument("--headless")

		chrome_options.page_load_strategy = 'normal'

		driver = uc.Chrome(options=chrome_options)

		driver.get('https://www.google.com/')

		time.sleep(randint(1,3))

		input = driver.find_element(By.XPATH, "//input[@name='q']")
		input.send_keys(nomeEmpresa)
		input.send_keys(Keys.ENTER)
		time.sleep(3)

		reviews = []

		# driver.find_element_by_link_text("Ver todos os comentários do Google").click()
		driver.find_element_by_xpath('//a[@data-sort_by="qualityScore"]').click()
		time.sleep(3)

		nomeLocal = self.getTitulo(driver)
		nota = self.getNota(driver)
		numeroAvaliacoes = self.getNumeroAvaliacao(driver)
		endereco = self.getEndereco(driver)
		try:
			cidade = endereco.split(',')[2].split('-')[0]
		except:
			cidade = ''
		try:
			estado = endereco.split(',')[2].split('-')[1]
		except:
			estado = ''

		driver.execute_script("document.querySelector('div.AxAp9e:nth-child(2)').click();")

		time.sleep(randint(1,3))

		naoChegou = True
		contador = 0
		while naoChegou:
			try:
				driver.execute_script("document.querySelector('.review-dialog-list').scrollTop = 1000000;")

				time.sleep(randint(2,4))

				soup = BeautifulSoup(driver.page_source, 'html.parser')
				div = soup.find('div',{'id':'reviewSort'})

				divReviews = div.find_all('div',{'class':'gws-localreviews__google-review'})

				for post in divReviews:
					nomeUsuario = post.find('div',{'class':'TSUbDb'}).getText()
					notaReview = post.find('span',{'class':'Fam1ne'}).get('aria-label')
					dataReview = post.find('span',{'class':'dehysf'}).getText()
					review = post.find('div',{'class':'Jtu6Td'}).getText()

					itemReview = {
						'nomeLocal':nomeLocal,
						'nomeUsuario':nomeUsuario,
						'notaReview':notaReview,
						'dataReview':dataReview,
						'review':review
					}

					if not self.filter(reviews, 'nomeUsuario', nomeUsuario):
						reviews.append(itemReview)
						contador+=1
						print("bucando review google:"+str(contador))
					
					if contador >= int(qtdReview):
						naoChegou = False
						break

			except:
				pass

		dados = {
			'nomeLocal':nomeLocal,
			'nota':nota.split(' ')[0],
			'numeroAvaliacoes':numeroAvaliacoes,
			'endereco':endereco,
			'cidade':cidade,
			'estado':estado,
			'reviews':reviews,
		}

		driver.quit()
		return dados