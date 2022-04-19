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

class Ifood():
    def filter(self, array, key, value):
        keyValList = [value]
        expectedResult = [d for d in array if d[key] in keyValList]
        return len(expectedResult) > 0

    def get(self, url, qtdReview):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--kiosk-printing')
        chrome_options.add_argument("--headless")

        chrome_options.page_load_strategy = 'normal'

        driver = uc.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(randint(2, 4))

        driver.execute_script("document.querySelector('#__next > div:nth-child(1) > main > div.restaurant-container > div > header.merchant-info > div.merchant-info__content-container > div > div.merchant-info__detail-container > button').click();")

        htmlVerMais = BeautifulSoup(driver.page_source, 'html.parser')

        driver.execute_script("document.querySelector('body > div.drawer > div > div > button').click();")
        time.sleep(randint(2, 4))

        driver.execute_script("document.querySelector('#__next > div:nth-child(1) > main > div.restaurant-container > div > header.merchant-info > div.merchant-info__content-container > div > div.merchant-info__title-container > div > a > button').click();")

        reviews = []
        naoChegou = True
        contador = 0
        contadorTentativa = 0
        while naoChegou:
            htmlNotas = BeautifulSoup(driver.page_source, 'html.parser')

            divReviews  = htmlNotas.find_all('div', {'class': 'rating-evaluation__wrapper'})

            for post in divReviews:
                nomeLocal = htmlNotas.find('p', {'class': 'rating-container__merchant'}).getText()
                try:
                    review = post.find('p', {'class': 'rating-evaluation__user'}).getText()
                except:
                    review = ''     
                notaReview = post.find('span', {'class': 'rating-evaluation-header__rate'}).getText()
                dataReview = post.find('span', {'class': 'rating-evaluation-header__date'}).getText()
                nomeUsuario = post.find('span', {'class': 'rating-evaluation-header__username'}).getText()

                itemReview = {
                    'nomeLocal': nomeLocal,
                    'review': review,
                    'notaReview': notaReview,
                    'dataReview': dataReview,
                    'nomeUsuario': nomeUsuario,
                }

                if not self.filter(reviews, 'nomeUsuario', nomeUsuario):
                    reviews.append(itemReview)
                    contador+=1
                    print("bucando review ifood:"+str(contador))
                else: 
                    contadorTentativa+=1
                
                if contadorTentativa >= 100:
                    naoChegou = False
                    break

                if contador >= int(qtdReview):
                    naoChegou = False
                    break
            driver.execute_script("document.querySelector('.rating-container').scrollTop = 1000000;")
            

        endereco = htmlVerMais.find_all('p', {'class': 'merchant-details-about__info-data'})[0].getText()+', '+htmlVerMais.find_all('p', {'class': 'merchant-details-about__info-data'})[1].getText()+', '+htmlVerMais.find_all('p', {'class': 'merchant-details-about__info-data'})[2].getText(),
        
        dados = {
            'nomeLocal': htmlNotas.find('p', {'class': 'rating-container__merchant'}).getText(),
            'nota': htmlNotas.find('p', {'class': 'rating-counter__average'}).getText(),
            'numeroAvaliacoes': htmlNotas.find('h3', {'class': 'rating-counter__total'}).getText().split(' ')[0],
            'endereco': endereco[0],
            'cnpj': htmlVerMais.find_all('p', {'class': 'merchant-details-about__info-data'})[3].getText().replace('CNPJ: ', ''),
            'reviews': reviews,
        }

        driver.quit()
        return dados
