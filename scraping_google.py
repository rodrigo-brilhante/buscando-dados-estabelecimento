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

def getTitulo(driver):
    try:
        return driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div/h2/span').text.strip()
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def getNota(driver):
    try:
        return driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div/span[1]').text.strip()
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def getNumeroAvaliacao(driver):
    try:
        return driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div/span[3]/span/a/span').text.strip()
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def getEndereco(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, '#kp-wp-tab-overview > div.TzHB6b.cLjAic.LMRCfc > div > div > div > div > div > div:nth-child(4) > div > div > div > span.LrzXr').text.strip()
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def getCidade(driver):
    try:
        return driver.find_element(By.XPATH, '//*[@id="_t2ZNYrfwC7_Z1sQPmPGcoAs44"]/div[1]/div[2]/div[1]/div/div/h2').text.strip()
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def getUrlIFood(driver):
    try:
        return driver.find_element(By.XPATH, '//*[@id="kp-wp-tab-overview"]/div[8]/div/div/div/div[1]/div/div/div[2]/div/a[1]').get_attribute('href')
    except Exception as ex:
        print("*****************************************\n",ex)
        return ''

def filter(array, key, value):
        keyValList = [value]
        expectedResult = [d for d in array if d[key] in keyValList]
        return len(expectedResult) > 0


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_argument("--headless")

    chrome_options.page_load_strategy = 'normal'

    nomeEmpresa = sys.argv[1]

    driver = uc.Chrome(options=chrome_options)

    driver.get('https://www.google.com/')

    time.sleep(randint(1,3))

    input = driver.find_element(By.XPATH, "//input[@name='q']")
    input.send_keys(nomeEmpresa)
    input.send_keys(Keys.ENTER)

    nomeLocal = getTitulo(driver)
    nota = getNota(driver)
    numeroAvaliacoes = getNumeroAvaliacao(driver)
    endereco = getEndereco(driver)
    cidade = endereco.split(',')[2].split('-')[0]
    estado = endereco.split(',')[2].split('-')[1]

    reviews = []

    driver.find_element_by_link_text("Ver todos os coment??rios do Google").click()

    time.sleep(randint(1,3))

    driver.execute_script("document.querySelector('div.AxAp9e:nth-child(2)').click();")

    time.sleep(randint(1,3))

    naoChegou = True
    while naoChegou:
        driver.execute_script("document.querySelector('.review-dialog-list').scrollTop = 10000;")

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
                'nomeUsuario':nomeUsuario,
                'notaReview':notaReview,
                'dataReview':dataReview,
                'review':review
            }
            if '3 meses' in dataReview:
                naoChegou = False
                break

            if not filter(reviews, 'nomeUsuario', nomeUsuario):
                reviews.append(itemReview)

    dados = {
        'nomeLocal':nomeLocal,
        'nota':nota.split(' ')[0],
        'numeroAvaliacoes':numeroAvaliacoes,
        'endereco':endereco,
        'cidade':endereco.split(',')[2].split('-')[0],
        'estado':endereco.split(',')[2].split('-')[1],
        'reviews':reviews,
    }

    driver.quit()

    print(json.dumps(dados))