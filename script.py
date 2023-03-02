import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

options = Options()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')

sleep(0.5)

navegador.find_element(By.TAG_NAME, 'button').click()

navegador.find_element(By.ID, '/homes-1-input').click()

cidade_desejada = input('Qual localidade deseja buscar? ')

navegador.find_element(By.ID, '/homes-1-input').send_keys(cidade_desejada)

navegador.find_element(By.ID, '/homes-1-input').submit()

navegador.find_element(By.CSS_SELECTOR, 'footer > button').click()

navegador.find_element(By.XPATH, '//*[@id="stepper-adults"]/button[2]').click() 
navegador.find_element(By.XPATH, '//*[@id="stepper-adults"]/button[2]').click() 

navegador.find_elements(By.TAG_NAME, 'button')[-1].click()

sleep(4)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

bloco_hospedagem = site.find_all('div', attrs={'itemprop': 'itemListElement'})

apartamento = []
 
for hospedagem in bloco_hospedagem:
    titulo = hospedagem.find('meta', attrs={'itemprop':'name'})
    titulo = titulo['content']
    link = hospedagem.find('meta', attrs={'itemprop':'url'})
    link = link['content']
    local = hospedagem.find('div', attrs={'class':'t1jojoys dir dir-ltr'})
    local = local.text
    if hospedagem.find('span', attrs={'class': '_1y74zjx'}):
        valor = hospedagem.find('span', attrs={'class': '_1y74zjx'})
        valor = valor.text
    elif hospedagem.find('span', attrs={'class': '_1ks8cgb'}):
        valor = hospedagem.find('span', attrs={'class': '_1ks8cgb'})
        valor = valor.text
    else:
        valor = hospedagem.find('span', attrs={'class': '_tyxjp1'})
        valor = valor.text
    apartamento.append([titulo, local, valor, link])
tabela = pd.DataFrame(apartamento, columns=['Nome', 'Local', 'Valor', 'URL'])
tabela.to_csv('./selenium-airbnb/lista_hospedagem_'+ cidade_desejada.lower().replace(' ', '_') + '.csv', index=False)