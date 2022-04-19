# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime
from django import template
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
from apps.home.tripadvisor import Tripadvisor
from apps.home.google import Google
from apps.home.reclame_aqui import ReclameAqui
from apps.home.ifood import Ifood
import os
import uuid

@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index", "resultsTripadvisor":[], "resultsIfood":[], "resultsReclame":[]}
    try:
        if request.GET["query"]:
            context["resultsTripadvisor"]=buscarTripadivisor(request.GET["query"])
            context["resultsReclame"]=buscarReclame(request.GET["query"])
            context["resultsIfood"]=buscarIfood(request.GET["query"])
    except:
        pass
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
# def detalhes(request):
#     context = {"segment": "index", "results":[]}
#     dados=request.GET["dados"]
#     context["dados"]=dados
#     html_template = loader.get_template("home/detalhes.html")
#     return HttpResponse(html_template.render(context))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
# def busca_estabelecimento(request):
#     context = {"results":buscar(request.GET["query"])}
#     return JsonResponse(context)

def buscarTripadivisor(query):
        query=query.replace(" ", "%20")
        url = f"https://www.tripadvisor.com.br/TypeAheadJson?interleaved=true&geoPages=true&details=true&types=geo%2Chotel%2Ceat%2Cattr%2Cvr%2Cair%2Ctheme_park%2Cal%2Cact%2Ccar%2Cship&neighborhood_geos=true&link_type=geo&matchTags=true&matchGlobalTags=true&matchKeywords=true&matchOverview=true&matchUserProfiles=true&strictAnd=false&scoreThreshold=0.8&hglt=true&disableMaxGroupSize=true&max=10&injectNewLocation=true&injectLists=true&nearby=true&local=true&parentids=&scope=-1&beforeGeoId=1&afterGeoId=&typeahead1_5=true&geoBoostFix=true&nearPages=true&nearPagesLevel=strict&rescue=true&supportedSearchTypes=find_near_stand_alone_query&query={query}&action=API&uiOrigin=MASTHEAD&source=MASTHEAD&startTime=1648321771073&searchSessionId=38AECBC29612816DA58451FF580D70F41648320967965ssid"

        headers = CaseInsensitiveDict()
        headers["authority"] = "www.tripadvisor.com.br"
        headers["cache-control"] = "max-age=0"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["upgrade-insecure-requests"] = "1"
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        headers["sec-fetch-site"] = "none"
        headers["sec-fetch-mode"] = "navigate"
        headers["sec-fetch-user"] = "?1"
        headers["sec-fetch-dest"] = "document"
        headers["accept-language"] = "pt-BR,pt;q=0.9"
        headers["cookie"] = "TADCID=br9ffQsJmqNnVl73ABQCFdpBzzOuRA-9xvCxaMyI12xqbmSZP4sOMygn2VxM3onKTN7n0ENcBvGT-6p2eEkrnT0XOG0IcLgXWAQ; TAUnique=%1%enc%3AE4zfPo0JW7GLVSZ%2Fu4S8bLmY3%2Fp0SOalVAYNOY1akLiF5oaXDAQCIA%3D%3D; __vt=bbXKiKwqHU5j3jQwABQCIf6-ytF7QiW7ovfhqc-AvRxIDr_No6IT2WMb6LUP4lyOyKimsZRG59IkmdZuQ0Z4lNg1zUz4qw5YuQrpuvNmFr7B_VbbOCG5uLor010NVlgxDqSdzzqe9hQVNHpTgc9L8xxSUA; SRT=TART_SYNC; TART=%1%enc%3Ai1Umf7uEvGzSsPzX7Pg6%2FharGJxjLv%2BhSQ%2BXt6GNZ%2BjsBgZKnBoAuXmJfeY3MT%2BAdQVMXpN2Oqc%3D; TASID=EFD65EC550F44A05BFE1440F1B09A598; ak_bmsc=A24C0AD656FB448EB68602AE36919C50~000000000000000000000000000000~YAAQRhc2F+XQjZt/AQAA3DCmxw8uEgNfG4/nD0UFgqUU++Vto2lu+84Qw4oghxdTyoj7krRtLDRqu3378M/XgYgXbqafthBMWSBnHvuVe9L2A+tT4P5DZbp/ke15xu//cC588xZX7d5Yux5pRHqpetf2grn5Kh4EP2i/CJezXvZV+e1eneubJSNNjfSP5yGCuUwBZOSgfwXVgQZfxiIh07XBHdvK/1SM25LfZDcsNlaSGL+9UI+WMmnCqrqQ5R4FT5R7QEYwdWzcgF9OXBRSkXJY7r0uZtakJizu8V175CeCkNprOAceSoPmCRbORDTV9kAWQfkAf1nRm5yaPOd0MMtb9Pssv+ZvTo6P65aWjZ1TxtxMNU0QIkE7bQzBpIPDPYQib44PfTQ1ur18o2MVks0G"

        resp = requests.get(url, headers=headers)
        results=resp.json()["results"]
        retorno=[]
        for result in results:
            try:
                if "Todos os resultados para" not in result["name"]:
                    if result["name"] and result["address"]:
                        retorno.append(result)
            except:
                pass
        return retorno

def buscarReclame(query):
        query=query.replace(" ", "%20")
        url = f"https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/{query}"

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

        resp = requests.get(url, headers=headers)
        results=resp.json()["companies"]
        retorno=[]
        for result in results:
            try:
                if result["companyName"] and result["shortname"]:
                    retorno.append(result)
            except:
                pass
        return retorno

def buscarIfood(query):
        query=query.replace(" ", "+")
        url = f"https://marketplace.ifood.com.br/v2/search/merchants?latitude=-23.5588276&longitude=-46.6599882&channel=IFOOD&term={query}&size=30&page=0"

        headers = CaseInsensitiveDict()
        headers["authority"] = "marketplace.ifood.com.br"
        headers["accept"] = "application/json, text/plain, */*"
        headers["accept-language"] = "pt-BR,pt;q=1"
        headers["app_version"] = "9.71.0"
        headers["browser"] = "Windows"
        headers["cache-control"] = "no-cache, no-store"
        headers["merchant_experiment_details"] = '{"default_merchant": {"model_id": "search-rerank","recommendation_filter": "AVAILABLE_FOR_SCHEDULING_FIXED", "available_for_scheduling_recommended_limit": 5, "engine": "sagemaker", "backend_experiment_id": "v4", "query_rewriter_model_id": "ifood-ml-c3po", "second_search": true, "similar_search": { "backend_experiment_id": "v2"}}}'
        headers["merchant_experiment_variant"] = "default_merchant"
        headers["newrelic"] = "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6Ijg5ODYyNiIsImFwIjoiMTY1MzIyNjI2OCIsImlkIjoiMGFjZjFiZDk5NWZkNzliOSIsInRyIjoiYTAyM2ZhMGVjYjZiNTc1YmU4OWZlNmI0MTZiZDA0YzAiLCJ0aSI6MTY0OTg0OTQ2OTI4Nn19"
        headers["origin"] = "https://www.ifood.com.br"
        headers["platform"] = "Desktop"
        headers["referer"] = "https://www.ifood.com.br/"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["sec-fetch-dest"] = "empty"
        headers["sec-fetch-mode"] = "cors"
        headers["sec-fetch-site"] = "same-site"
        headers["traceparent"] = "00-a023fa0ecb6b575be89fe6b416bd04c0-0acf1bd995fd79b9-01"
        headers["tracestate"] = "898626@nr=0-1-898626-1653226268-0acf1bd995fd79b9----1649849469286"
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        headers["x-ifood-device-id"] = "f980cd14-677f-4e3c-a549-1be49ff20b75"
        headers["x-ifood-session-id"] = "bdec9988-b9a7-42ea-b710-c02943d97d0a"

        resp = requests.get(url, headers=headers)
        results=resp.json()["merchants"]["data"]
        retorno=[]
        for result in results:
            try:
                if result["name"] and result["slug"]:
                    result["url"] = result["slug"] + "/" + result["id"]
                    retorno.append(result)
            except:
                pass
        return retorno

def buscar_review(request):
    context = {"segment": "index", "dados":[]}

    if request.method == "GET":
        tripadvisor=Tripadvisor()
        google=Google()
        ifood=Ifood()
        reclameAqui=ReclameAqui()

        qtdReview=request.GET["qtdReview"]

        urlsTrip=request.GET["urlTrivadisor"].split(";")
        urlsReclame=request.GET["urlsReclame"].split(";")
        urlsGoogle=request.GET["urlsGoogle"].split(";")
        urlsIfood=request.GET["urlsIfood"].split(";")
     
        dadoTripadvisor=[]
        dadoReclameAqui=[]
        dadoGoogle=[]
        dadosIfood=[]

        for url in urlsTrip:
            if url != '':
                try:
                    dadoTripadvisor.append(tripadvisor.get("https://www.tripadvisor.com.br/"+url, qtdReview))
                except:
                    pass
        for nomeEmpresa in urlsReclame:
            if nomeEmpresa != '':
                try:
                    dadoReclameAqui.append(reclameAqui.get(nomeEmpresa, qtdReview))
                except:
                    pass

        for nomeEmpresa in urlsGoogle:
            if nomeEmpresa != '':
                try:
                    dadoGoogle.append(google.get(nomeEmpresa, qtdReview))
                except:
                    pass

        for url in urlsIfood:
            if url != '':
                try:
                    dadosIfood.append(ifood.get("https://www.ifood.com.br/delivery/"+url, qtdReview))
                except:
                    pass
                

        dados = {
            "tripadvisor":dadoTripadvisor,
            "reclameAqui":dadoReclameAqui,
            "google":dadoGoogle,
            "ifood":dadosIfood
        }
        
        name=gerar_excel(dados)
        
        context["dados"]=dados
        context["path_excel"]=name

        html_template = loader.get_template("home/detalhes.html")
        return HttpResponse(html_template.render(context))

def gerar_excel(dados):
    
    notasTripadvisor=[]
    reviewsTripadvisor=[]
    notasReclameAqui=[]
    reviewsReclameAqui=[]
    notasGoogle=[]
    reviewsGoogle=[]
    notasIfood=[]
    reviewsIfood=[]
    for dado in dados["tripadvisor"]:
        # extraindo dados Tripadvisor
        try:
            nota=dado["notas"]
            for r in dado["reviews"]:
                reviewsTripadvisor.append({
                    "local": r["local"],
                    "review":r["review"],
                    "nota": r["nota"],
                    "dataReview": r["dataReview"],
                    "cidadeLocal": r["cidadeLocal"]
                })
            notasTripadvisor.append({
                "cidade": nota["cidade"],
                "endereco": nota["endereco"],
                "localidadeRanking": nota["localidadeRanking"],
                "nome": nota["nome"],
                "notaGeral": nota["notaGeral"],
                "numeroAvaliacoes": nota["numeroAvaliacoes"],
                "pontuacaoComida": nota["pontuacaoComida"],
                "pontuacaoPreco": nota["pontuacaoPreco"],
                "pontuacaoServico": nota["pontuacaoServico"],
                "pontuacaAmbiente": nota["pontuacaAmbiente"],
                "ranking": nota["ranking"],
                "telefone": nota["telefone"],
                "breakdown_nota_1": nota["breakdownNotas"]["nota_1"],
                "breakdown_nota_2": nota["breakdownNotas"]["nota_2"],
                "breakdown_nota_3": nota["breakdownNotas"]["nota_3"],
                "breakdown_nota_4": nota["breakdownNotas"]["nota_4"],
                "breakdown_nota_5": nota["breakdownNotas"]["nota_5"],
            })
        except:
            pass
    for dado in dados["reclameAqui"]:
        # extraindo dados Reclame Aqui
        try:
            nota=dado
            for r in dado["reviews"]:
                reviewsReclameAqui.append({
                    "nomeLocal": r["nomeLocal"],
                    "tituloReview":r["tituloReview"],
                    "review": r["review"],
                    "data": r["data"],
                    "status": r["status"],
                })
            notasReclameAqui.append({
                "nomeLocal": nota["nomeDoLocal"],
                
                "pontuacaoFinalGeral":nota["avaliacaoes"][4]["pontuacaoFinal"],
                "percentualRespondidoGeral":nota["avaliacaoes"][4]["percentualRespondido"],
                "percentualVoltariamAfazerNegocioGeral":nota["avaliacaoes"][4]["percentualVoltariamAfazerNegocio"],
                "percentualResolvidoGeral":nota["avaliacaoes"][4]["percentualResolvido"],
                "totalReclamacoesGeral":nota["avaliacaoes"][4]["totalReclamacoes"],
                
                "pontuacaoFinal6meses":nota["avaliacaoes"][0]["pontuacaoFinal"],
                "percentualRespondido6meses":nota["avaliacaoes"][0]["percentualRespondido"],
                "percentualVoltariamAfazerNegocio6meses":nota["avaliacaoes"][0]["percentualVoltariamAfazerNegocio"],
                "percentualResolvido6meses":nota["avaliacaoes"][0]["percentualResolvido"],
                "totalReclamacoes6meses":nota["avaliacaoes"][0]["totalReclamacoes"],
                
                "pontuacaoFinal12meses":nota["avaliacaoes"][1]["pontuacaoFinal"],
                "percentualRespondido12meses":nota["avaliacaoes"][1]["percentualRespondido"],
                "percentualVoltariamAfazerNegocio12meses":nota["avaliacaoes"][1]["percentualVoltariamAfazerNegocio"],
                "percentualResolvido12meses":nota["avaliacaoes"][1]["percentualResolvido"],
                "totalReclamacoes12meses":nota["avaliacaoes"][1]["totalReclamacoes"],
                
                "pontuacaoFinal1ano":nota["avaliacaoes"][2]["pontuacaoFinal"],
                "percentualRespondido1ano":nota["avaliacaoes"][2]["percentualRespondido"],
                "percentualVoltariamAfazerNegocio1ano":nota["avaliacaoes"][2]["percentualVoltariamAfazerNegocio"],
                "percentualResolvido1ano":nota["avaliacaoes"][2]["percentualResolvido"],
                "totalReclamacoes1ano":nota["avaliacaoes"][2]["totalReclamacoes"],
                
                "pontuacaoFinal2ano":nota["avaliacaoes"][3]["pontuacaoFinal"],
                "percentualRespondido2ano":nota["avaliacaoes"][3]["percentualRespondido"],
                "percentualVoltariamAfazerNegocio2ano":nota["avaliacaoes"][3]["percentualVoltariamAfazerNegocio"],
                "percentualResolvido2ano":nota["avaliacaoes"][3]["percentualResolvido"],
                "totalReclamacoes2ano":nota["avaliacaoes"][3]["totalReclamacoes"],
                
                "problema1porcentagem":nota["problemas"]["problema1"]["porcentagem"],
                "problema1motivo":nota["problemas"]["problema1"]["motivo"],
                
                "problema2porcentagem":nota["problemas"]["problema2"]["porcentagem"],
                "problema2motivo":nota["problemas"]["problema2"]["motivo"],
                
                "problema3porcentagem":nota["problemas"]["problema3"]["porcentagem"],
                "problema3motivo":nota["problemas"]["problema3"]["motivo"],
            })
        except:
            pass
        # Fim Reclame Aqui
    for dado in dados["google"]:
        # extraindo dados google
        try:
            nota=dado
            for r in dado["reviews"]:
                reviewsGoogle.append({
                    "nomeLocal": r["nomeLocal"],
                    "nomeUsuario": r["nomeUsuario"],
                    "notaReview": r["notaReview"],
                    "dataReview": r["dataReview"],
                    "review": r["review"],
                })
            notasGoogle.append({
                "nomeLocal": nota["nomeLocal"],
                "nota": nota["nota"],
                "numeroAvaliacoes":nota["numeroAvaliacoes"],
                "endereco": nota["endereco"],
                "cidade": nota["cidade"],
                "estado": nota["estado"]
            })
        except:
            pass
        # fim google
    for dado in dados["ifood"]:
        # extraindo dados ifood
        try:
            nota=dado
            for r in dado["reviews"]:
                reviewsIfood.append({
                    "nomeLocal": r["nomeLocal"],
                    "review": r["review"],
                    "notaReview":r["notaReview"],
                    "dataReview": r["dataReview"],
                    "nomeUsuario": r["nomeUsuario"],
                })
            notasIfood.append({
                "nomeLocal": nota["nomeLocal"],
                "nota": nota["nota"],
                "numeroAvaliacoes": nota["numeroAvaliacoes"],
                "endereco": nota["endereco"][0],
                "cnpj": nota["cnpj"],
            })
        except:
            pass
        # fim ifodod

    # organizando os dados Tripadvisor
    dataTripadvisor={
        "Nome": [str(x["nome"]) for x in notasTripadvisor], 
        "# de Avaliações": [str(x["numeroAvaliacoes"]) for x in notasTripadvisor], 
        "Nota Geral": [str(x["notaGeral"]) for x in notasTripadvisor],
        "5": [str(x["breakdown_nota_5"]) for x in notasTripadvisor],
        "4": [str(x["breakdown_nota_4"]) for x in notasTripadvisor],
        "3": [str(x["breakdown_nota_3"]) for x in notasTripadvisor],
        "2": [str(x["breakdown_nota_2"]) for x in notasTripadvisor],
        "1": [str(x["breakdown_nota_1"]) for x in notasTripadvisor],
        "Pontuação Comida": [str(x["pontuacaoComida"]) for x in notasTripadvisor], 
        "Pontuação Serviço": [str(x["pontuacaoServico"]) for x in notasTripadvisor],
        "Pontuação Preço": [str(x["pontuacaoPreco"]) for x in notasTripadvisor],
        "Pontuação Ambiente": [str(x["pontuacaAmbiente"]) for x in notasTripadvisor],
        "Ranking": [str(x["ranking"]) for x in notasTripadvisor], 
        "Localidade do Ranking": [str(x["localidadeRanking"]) for x in notasTripadvisor], 
        "Cidade": [str(x["cidade"]) for x in notasTripadvisor],
        "Endereço": [str(x["endereco"]) for x in notasTripadvisor], 
        "Telefone": [str(x["telefone"]) for x in notasTripadvisor]
    }

    df1 = pd.DataFrame(dataTripadvisor, columns = ["Nome", "# de Avaliações", 
    "Nota Geral","5","4","3","2","1",
    "Pontuação Comida", "Pontuação Serviço","Pontuação Preço","Pontuação Ambiente",
    "Ranking", "Localidade do Ranking", "Cidade",
    "Endereço", "Telefone"])

    dataTripadvisor={
        "Local": [str(x["local"]) for x in reviewsTripadvisor], 
        "Review": [str(x["review"]) for x in reviewsTripadvisor], 
        "Nota": [str(x["nota"]) for x in reviewsTripadvisor],
        "Data Review": [str(x["dataReview"]) for x in reviewsTripadvisor],
        "Cidade do Local": [str(x["cidadeLocal"]) for x in reviewsTripadvisor],
    }

    df2 = pd.DataFrame(dataTripadvisor, columns=["Local", "Review", "Nota", "Data Review", "Cidade do Local"])  
    # fim Tripadvisor

    # organizando os dados Reclame Aqui
    dataReclameAqui={
        "Nome do Local":[str(x["nomeLocal"]) for x in notasReclameAqui], 
        
        "Nota Geral":[str(x["pontuacaoFinalGeral"]) for x in notasReclameAqui], 
        "% Respondidas":[str(x["percentualRespondidoGeral"]) for x in notasReclameAqui],
        "% Volta Negócio":[str(x["percentualVoltariamAfazerNegocioGeral"]) for x in notasReclameAqui], 
        "Índice Solução":[str(x["percentualResolvidoGeral"]) for x in notasReclameAqui], 
        "# Reclamações":[str(x["totalReclamacoesGeral"]) for x in notasReclameAqui], 

        "Nota 6 Meses":[str(x["pontuacaoFinal6meses"]) for x in notasReclameAqui], 
        "% Respondidas":[str(x["percentualRespondido6meses"]) for x in notasReclameAqui], 
        "% Volta Negócio":[str(x["percentualVoltariamAfazerNegocio6meses"]) for x in notasReclameAqui], 
        "Índice Solução":[str(x["percentualResolvido6meses"]) for x in notasReclameAqui], 
        "# Reclamações":[str(x["totalReclamacoes6meses"]) for x in notasReclameAqui], 
        
        "Nota 12 Meses":[str(x["pontuacaoFinal12meses"]) for x in notasReclameAqui], 
        "% Respondidas":[str(x["percentualRespondido12meses"]) for x in notasReclameAqui], 
        "% Volta Negócio":[str(x["percentualVoltariamAfazerNegocio12meses"]) for x in notasReclameAqui], 
        "Índice Solução":[str(x["percentualResolvido12meses"]) for x in notasReclameAqui], 
        "# Reclamações":[str(x["totalReclamacoes12meses"]) for x in notasReclameAqui], 
        
        "Nota Ano -1":[str(x["pontuacaoFinal1ano"]) for x in notasReclameAqui], 
        "% Respondidas":[str(x["percentualRespondido1ano"]) for x in notasReclameAqui], 
        "% Volta Negócio":[str(x["percentualVoltariamAfazerNegocio1ano"]) for x in notasReclameAqui], 
        "Índice Solução":[str(x["percentualResolvido1ano"]) for x in notasReclameAqui], 
        "# Reclamações":[str(x["totalReclamacoes1ano"]) for x in notasReclameAqui], 

        "Nota Ano -2":[str(x["pontuacaoFinal2ano"]) for x in notasReclameAqui], 
        "% Respondidas":[str(x["percentualRespondido2ano"]) for x in notasReclameAqui], 
        "% Volta Negócio":[str(x["percentualVoltariamAfazerNegocio2ano"]) for x in notasReclameAqui], 
        "Índice Solução":[str(x["percentualResolvido2ano"]) for x in notasReclameAqui], 
        "# Reclamações":[str(x["totalReclamacoes2ano"]) for x in notasReclameAqui], 
    
        "1 - %":[str(x["problema1porcentagem"]) for x in notasReclameAqui],
        "1 - Motivo":[str(x["problema1motivo"]) for x in notasReclameAqui],
        
        "2 - %":[str(x["problema2porcentagem"]) for x in notasReclameAqui],
        "2 - Motivo":[str(x["problema2motivo"]) for x in notasReclameAqui],
        
        "3 - %":[str(x["problema3porcentagem"]) for x in notasReclameAqui],
        "3 - Motivo":[str(x["problema3motivo"]) for x in notasReclameAqui],
    }

    
    df3 = pd.DataFrame(dataReclameAqui, columns=["Nome do Local", "Nota Geral", "% Respondidas", "% Volta Negócio", "Índice Solução", "# Reclamações", "Nota 6 Meses", "% Respondidas", "% Volta Negócio", "Índice Solução", "# Reclamações", "Nota 12 Meses", "% Respondidas", "% Volta Negócio", "Índice Solução", "# Reclamações", "Nota Ano -1", "% Respondidas", "% Volta Negócio", "Índice Solução", "# Reclamações", "Nota Ano -2", "% Respondidas", "% Volta Negócio", "Índice Solução", "# Reclamações", "1 - %", "1 - Motivo", "2 - %", "2 - Motivo", "3 - %", "3 - Motivo"])  

    dataReclameAqui={ 
        "Nome do Local":[str(x["nomeLocal"]) for x in reviewsReclameAqui], 
        "Título do Review":[str(x["tituloReview"]) for x in reviewsReclameAqui], 
        "Review":[str(x["review"]) for x in reviewsReclameAqui], 
        "Data":[str(x["data"]) for x in reviewsReclameAqui], 
        "Status":[str(x["status"]) for x in reviewsReclameAqui]
    }
    df4 = pd.DataFrame(dataReclameAqui, columns=["Nome do Local", "Título do Review", "Review", "Data", "Status"])  
    # fim Reclame Aqui

    # organizando os dados Google
    dataGoogle={
        "Nome do Local": [str(x["nomeLocal"]) for x in notasGoogle], 
        "Nota": [str(x["nota"]) for x in notasGoogle], 
        "# de Avaliações": [str(x["numeroAvaliacoes"]) for x in notasGoogle],
        "Endereço": [str(x["endereco"]) for x in notasGoogle],
        "Cidade": [str(x["cidade"]) for x in notasGoogle],
        "Estado": [str(x["estado"]) for x in notasGoogle],
    }
    df5 = pd.DataFrame(dataGoogle, columns = ["Nome do Local", "Nota", "# de Avaliações", "Endereço", "Cidade", "Estado"])

    dataGoogle={
        "Nome do Local": [str(x["nomeLocal"]) for x in reviewsGoogle], 
        "Review": [str(x["review"]) for x in reviewsGoogle],
        "Nota do Review": [str(x["notaReview"]) for x in reviewsGoogle], 
        "Data do Review": [str(x["dataReview"]) for x in reviewsGoogle],
        "Nome do Usuário": [str(x["nomeUsuario"]) for x in reviewsGoogle], 
    }
    df6 = pd.DataFrame(dataGoogle, columns = ["Nome do Local", "Review", "Nota do Review", "Data do Review", "Nome do Usuário"])
    # Fim Google

    # organizando os dados iFood
    dataIfood={
        "Nome do Local": [str(x["nomeLocal"]) for x in notasIfood], 
        "Nota": [str(x["nota"]) for x in notasIfood], 
        "# de Avaliações": [str(x["numeroAvaliacoes"]) for x in notasIfood],
        "Endereço do Local": [str(x["endereco"]) for x in notasIfood],
        "CNPJ": [str(x["cnpj"]) for x in notasIfood],
    }
    df7= pd.DataFrame(dataIfood, columns = ["Nome do Local", "Nota", "# de Avaliações", "Endereço do Local", "CNPJ"])

    dataIfood={
        "Nome do Local": [str(x["nomeLocal"]) for x in reviewsIfood], 
        "Review": [str(x["review"]) for x in reviewsIfood],
        "Nota do Review": [str(x["notaReview"]) for x in reviewsIfood], 
        "Data do Review": [str(x["dataReview"]) for x in reviewsIfood],
        "Nome do Usuário": [str(x["nomeUsuario"]) for x in reviewsIfood]
    }
    df8 = pd.DataFrame(dataIfood, columns = ["Nome do Local", "Review", "Nota do Review", "Data do Review", "Nome do Usuário"])
    # fim iFood

    name = uuid.uuid4().hex+".xlsx"
    with pd.ExcelWriter("media/tmp-"+name) as writer:
        df1.to_excel(writer,index = False, header=True, sheet_name="Tripadvisor Notas",startcol=0)  
        df2.to_excel(writer,index = False, header=True, sheet_name="Tripadvisor Reviews",startcol=0)
        df3.to_excel(writer,index = False, header=True, sheet_name="ReclameAqui Notas",startcol=0)
        df4.to_excel(writer,index = False, header=True, sheet_name="ReclameAqui Reviews",startcol=0)
        df5.to_excel(writer,index = False, header=True, sheet_name="Google Notas",startcol=0)
        df6.to_excel(writer,index = False, header=True, sheet_name="Google Reviews",startcol=0)
        df7.to_excel(writer,index = False, header=True, sheet_name="iFood Notas",startcol=0)
        df8.to_excel(writer,index = False, header=True, sheet_name="iFoos Reviews",startcol=0)
    return name
    
def baixar_excel(request):
    name=request.GET["name"]
    file_path="media/tmp-"+name
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + datetime.datetime.now().strftime("%d-%m-%Y %H %M %S")+".xlsx"
            return response
    raise Http404