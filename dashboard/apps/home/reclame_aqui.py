from dataclasses import replace
from secrets import choice
import sys
import requests
from requests.structures import CaseInsensitiveDict
import warnings
from bs4 import BeautifulSoup
import json
from datetime import datetime
import random

class ReclameAqui():
    def getAvaliacao(self, avaliacao):
        periodo = {
            'SIX_MONTHS' : '6 meses',
            'TWELVE_MONTHS' : '12 meses',
            'LAST_YEAR' : '1 ano',
            'PAST_LAST_YEAR' : '2 anos',
            'LAST_THREE_YEARS' : '3 anos',
        }
        return {
            'periodo': periodo[avaliacao['type']],
            'pontuacaoFinal' : avaliacao['finalScore'],
            'percentualRespondido' : avaliacao['answeredPercentual'],
            'percentualVoltariamAfazerNegocio' : avaliacao['dealAgainPercentual'],
            'percentualResolvido' : avaliacao['solvedPercentual'],
            'totalReclamacoes' : avaliacao['totalComplains'],
        }

    def getProblemas(self, problemas):
        problema1 = {
            'porcentagem': problemas['problems'][0]['recorrencyPercentual'],
            'motivo': problemas['problems'][0]['name']
        }
        problema2 = {
            'porcentagem': problemas['products'][0]['recorrencyPercentual'],
            'motivo': problemas['products'][0]['name']
        }
        problema3 = {
            'porcentagem': problemas['categories'][0]['recorrencyPercentual'],
            'motivo': problemas['categories'][0]['name']
        }
        return {
            'problema1':problema1,
            'problema2':problema2,
            'problema3':problema3
        }

    def getReclamacoesNaoRespondidas(self, id):
        url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/complains/?company="+id+"&status=PENDING&evaluated=bool:false&index=0&offset=20&order=created&orderType=desc&deleted=bool:false&fields=evaluated,title,solved,userName,status,created,id,description"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://www.reclameaqui.com.br"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://www.reclameaqui.com.br/"
        headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"

        resp = requests.get(url, headers=headers)

        return json.loads(resp.text)

    def getReclamacoesRespondidas(self, id):
        url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/complains/?company="+id+"&status=ANSWERED&evaluated=bool:false&index=0&offset=20&order=created&orderType=desc&deleted=bool:false&fields=evaluated,title,solved,userName,status,created,id,description"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://www.reclameaqui.com.br"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://www.reclameaqui.com.br/"
        headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"

        resp = requests.get(url, headers=headers)

        return json.loads(resp.text)

    def getReclamacoesAvaliadas(self, id):
        url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/complains/?company="+id+"&evaluated=bool:true&index=0&offset=20&order=created&orderType=desc&deleted=bool:false&fields=evaluated,title,solved,userName,status,created,id,description"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://www.reclameaqui.com.br"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://www.reclameaqui.com.br/"
        headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"

        resp = requests.get(url, headers=headers)

        return json.loads(resp.text)

    def getReviews(self, id, nomeLocal):
        reclamacoesNaoRespondidas = self.getReclamacoesNaoRespondidas(id)
        reclamacoesRespondidas = self.getReclamacoesRespondidas(id)
        reclamacoesAvaliadas = self.getReclamacoesAvaliadas(id)

        dadosReviews = []
        status = {
            'PENDING':'Pendente',
            'ANSWERED':'Respondidos',
        }

        for review in reclamacoesNaoRespondidas['data']:
            dadosReviews.append({
                'nomeLocal':nomeLocal,
                'tituloReview':review['title'],
                'review':review['description'],
                'data':review['created'],
                'status':status[review['status']]
            })
        for review in reclamacoesRespondidas['data']:
            dadosReviews.append({
                'nomeLocal':nomeLocal,
                'tituloReview':review['title'],
                'review':review['description'],
                'data':review['created'],
                'status':status[review['status']]
            })
        for review in reclamacoesAvaliadas['data']:
            dadosReviews.append({
                'nomeLocal':nomeLocal,
                'tituloReview':review['title'],
                'review':review['description'],
                'data':review['created'],
                'status':status[review['status']]
            })
        
        return dadosReviews
        
    warnings.filterwarnings('ignore')

    def get(self, nome):
        with requests.Session() as session:
            try:
                url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/" + nome.replace(' ', '%20')

                headers = CaseInsensitiveDict()
                headers["Connection"] = "keep-alive"
                headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
                headers["Accept"] = "application/json, text/plain, */*"
                headers["sec-ch-ua-mobile"] = "?0"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
                headers["sec-ch-ua-platform"] = '"Windows"'
                headers["Origin"] = "https://www.reclameaqui.com.br"
                headers["Sec-Fetch-Site"] = "same-site"
                headers["Sec-Fetch-Mode"] = "cors"
                headers["Sec-Fetch-Dest"] = "empty"
                headers["Referer"] = "https://www.reclameaqui.com.br/"
                headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"

                resp = session.get(url, headers=headers)
                

                respJson = json.loads(resp.text)

                id = respJson['companies'][0]['id']
                shortname = respJson['companies'][0]['shortname']
                nomeDoLocal = respJson['companies'][0]['companyName']
                
                url = 'https://www.reclameaqui.com.br/empresa/'+shortname
                
                headers["Connection"] = "keep-alive"
                headers["Cache-Control"] = "max-age=0"
                headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
                headers["sec-ch-ua-mobile"] = "?0"
                headers["sec-ch-ua-platform"] = '"Windows"'
                headers["Upgrade-Insecure-Requests"] = "1"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                headers["Sec-Fetch-Site"] = "same-origin"
                headers["Sec-Fetch-Mode"] = "navigate"
                headers["Sec-Fetch-User"] = "?1"
                headers["Sec-Fetch-Dest"] = "document"
                headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"
                headers["Cookie"] = "__auc=76d7453d17e54ef3253318fdcfc; _hjid=11ac1814-4e89-4650-9c07-48074a9e2d73; _hjSessionUser_417945=eyJpZCI6IjZhZmMwNDQ4LTY1Y2QtNTZhNy1iN2Q0LTJjMmM5YTI2MmY3ZCIsImNyZWF0ZWQiOjE2NDIxMDI0Njk4NjksImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2022-01-13T19:34:32.896Z; _gid=GA1.3.1485515770.1648922295; visid_incap_2173072=1Qt4cytzTEi3f+49fyuYHLiOSGIAAAAAQUIPAAAAAACuwwniiqv0AfgJZF9jRD2p; UserClosedTouchpointPopup=true; _gac_UA-5435672-2=1.1649070018.CjwKCAjwrqqSBhBbEiwAlQeqGg0KeXui_X9PwtD1e5B3jE_I13faQzJoziGxjFo5pTobY3PNmA7RVhoCLsMQAvD_BwE; _hjDonePolls=795298; _gat_gtag_UA_5435672_2=1; __asc=994dcfc417ff905a1f33171d798; _ga_GQ3KZJ0431=GS1.1.1649150368.15.0.1649150368.0; _ga=GA1.1.1290617086.1642102469; incap_ses_1478_2173072=wP5qCdpagX794g43XOmCFKEJTGIAAAAAAMyaGY7d+ngsEg2Y8PmjRA==; _hjIncludedInSessionSample=1; _hjSession_417945=eyJpZCI6IjFkNjNkMDM0LWQyM2EtNDA2Ni04Yzc2LTgxMmI1OWFkMDk4ZiIsImNyZWF0ZWQiOjE2NDkxNTAzNzA5NzQsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Apr+05+2022+06%3A19%3A31+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.25.0&isIABGlobal=false&hosts=&consentId=64c452e7-0ae4-4d32-b395-1db5579d8e27&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false"
                headers["If-None-Match"] = '"35cb6-rvUBvk1FySqe5HhI7JNPiZ7noAw"'

                resp = session.get(url, headers=headers)
            
                aux = resp.text.split('type="application/json">')[1]
                aux = aux.replace('</script></body></html>', '')
                dados = json.loads(aux) 
                
                dadosAvaliacoes = dados['props']['pageProps']['company']['panels']
                
                avaliacaoes = []
                for avaliacao in dadosAvaliacoes:
                    avaliacaoes.append(self.getAvaliacao(avaliacao['index']))
                
                # buscar principais problemas
                url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyMainProblems/"+id

                headers = CaseInsensitiveDict()
                headers["Connection"] = "keep-alive"
                headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
                headers["Accept"] = "application/json, text/plain, */*"
                headers["sec-ch-ua-mobile"] = "?0"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
                headers["sec-ch-ua-platform"] = '"Windows"'
                headers["Origin"] = "https://www.reclameaqui.com.br"
                headers["Sec-Fetch-Site"] = "same-site"
                headers["Sec-Fetch-Mode"] = "cors"
                headers["Sec-Fetch-Dest"] = "empty"
                headers["Referer"] = "https://www.reclameaqui.com.br/"
                headers["Accept-Language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"

                resp = session.get(url, headers=headers)
                
                dados = json.loads(resp.text) 

                problemas = self.getProblemas(dados['complainResult']['complains'])
            
                reviews = self.getReviews(id, nomeDoLocal)
                
                dados = {
                    'nomeDoLocal':nomeDoLocal,
                    'avaliacaoes':avaliacaoes,
                    'problemas':problemas,
                    'reviews':reviews
                }
                return dados
            except Exception as ex:
                print(ex)
