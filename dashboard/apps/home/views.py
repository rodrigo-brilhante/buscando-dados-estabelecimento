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
import os
import uuid

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index', 'results':[]}
    try:
        if request.GET['query']:
            context["results"]=buscar(request.GET['query'])
    except:
        pass
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def busca_estabelecimento(request):
    context = {'results':buscar(request.GET['query'])}
    return JsonResponse(context)

def buscar(query):
        query=query.replace(' ', '%20')
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
        results=resp.json()['results']
        retorno=[]
        for result in results:
            try:
                if 'Todos os resultados para' not in result['name']:
                    if result['name'] and result['address']:
                        retorno.append(result)
            except:
                pass
        return retorno

def buscar_review(request):
    if request.method == 'POST':
        tripadvisor=Tripadvisor()
        urls=request.POST['urlTrivadisor'].split(';')
        dados=[]
        for url in urls:
            dado=tripadvisor.get('https://www.tripadvisor.com.br/'+url)
            dados.append(dado)
        name=gerar_excel(dados)
        return JsonResponse({'name':name})

def gerar_excel(dados):
    
    notas=[]
    reviews=[]
    for dado in dados:
        try:
            nota=dado['notas']
            for r in dado['reviews']:
                reviews.append({
                    'local': r['local'],
                    'review':r['review'],
                    'nota': r['nota'],
                    'dataReview': r['dataReview'],
                    'cidadeLocal': r['cidadeLocal']
                })
            notas.append({
                'cidade': nota['cidade'],
                'endereco': nota['endereco'],
                'localidadeRanking': nota['localidadeRanking'],
                'nome': nota['nome'],
                'notaGeral': nota['notaGeral'],
                'numeroAvaliacoes': nota['numeroAvaliacoes'],
                'pontuacaoComida': nota['pontuacaoComida'],
                'pontuacaoPreco': nota['pontuacaoPreco'],
                'pontuacaoServico': nota['pontuacaoServico'],
                'ranking': nota['ranking'],
                'telefone': nota['telefone'],
                'breakdown_nota_1': nota['breakdownNotas']['nota_1'],
                'breakdown_nota_2': nota['breakdownNotas']['nota_2'],
                'breakdown_nota_3': nota['breakdownNotas']['nota_3'],
                'breakdown_nota_4': nota['breakdownNotas']['nota_4'],
                'breakdown_nota_5': nota['breakdownNotas']['nota_5'],
            })
        except:
            pass
    
    data={
        "Nome": [str(x['nome']) for x in notas], 
        "# de Avaliações": [str(x['numeroAvaliacoes']) for x in notas], 
        "Nota Geral": [str(x['notaGeral']) for x in notas],
        "5": [str(x['breakdown_nota_5']) for x in notas],
        "4": [str(x['breakdown_nota_4']) for x in notas],
        "3": [str(x['breakdown_nota_3']) for x in notas],
        "2": [str(x['breakdown_nota_2']) for x in notas],
        "1": [str(x['breakdown_nota_1']) for x in notas],
        "Pontuação Comida": [str(x['pontuacaoComida']) for x in notas], 
        "Pontuação Serviço": [str(x['pontuacaoServico']) for x in notas],
        "Pontuação Preço": [str(x['pontuacaoPreco']) for x in notas],
        "Ranking": [str(x['ranking']) for x in notas], 
        "Localidade do Ranking": [str(x['localidadeRanking']) for x in notas], 
        "Cidade": [str(x['cidade']) for x in notas],
        "Endereço": [str(x['endereco']) for x in notas], 
        "Telefone": [str(x['telefone']) for x in notas]
    }

    df1 = pd.DataFrame(data, columns = ["Nome", "# de Avaliações", 
    "Nota Geral","5","4","3","2","1",
    "Pontuação Comida", "Pontuação Serviço","Pontuação Preço",
    "Ranking", "Localidade do Ranking", "Cidade",
    "Endereço", "Telefone"])

    data={
        "Local": [str(x['local']) for x in reviews], 
        "Review": [str(x['review']) for x in reviews], 
        "Nota": [str(x['nota']) for x in reviews],
        "Data Review": [str(x['dataReview']) for x in reviews],
        "Cidade do Local": [str(x['cidadeLocal']) for x in reviews],
    }

    df2 = pd.DataFrame(data, columns=["Local", "Review", "Nota", "Data Review", "Cidade do Local"])  

    name = uuid.uuid4().hex+'.xlsx'
    with pd.ExcelWriter('media/tmp-'+name) as writer:
        df1.to_excel(writer,index = False, header=True, sheet_name="Tripadvisor Notas",startcol=0)  
        df2.to_excel(writer,index = False, header=True, sheet_name="Tripadvisor Reviews",startcol=0)
    return name
    
def baixar_excel(request):
    name=request.GET['name']
    file_path='media/tmp-'+name
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + datetime.datetime.now().strftime("%d-%m-%Y %H %M %S")+'.xlsx'
            return response
    raise Http404