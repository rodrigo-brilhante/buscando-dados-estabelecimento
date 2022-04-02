from secrets import choice
import sys
import requests
from requests.structures import CaseInsensitiveDict
import warnings
from bs4 import BeautifulSoup
import json
from datetime import datetime
import random


warnings.filterwarnings('ignore')

def MesLimite():
    return {
        '01' : 'outubro',
        '02' : 'novembro',
        '03' : 'dezembro',
        '04' : 'janeiro',
        '05' : 'fevereiro',
        '06' : 'março',
        '07' : 'abril',
        '08' : 'maio',
        '09' : 'junho',
        '10' : 'julho',
        '11' : 'agosto',
        '12' : 'setembro',
    }[datetime.today().strftime('%m')]
    
url = sys.argv[1]

with requests.Session() as session:
    try:
        headers = CaseInsensitiveDict()
        headers["authority"] = "www.tripadvisor.com.br"
        headers["cache-control"] = "max-age=0"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["upgrade-insecure-requests"] = "1"
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        headers["sec-fetch-site"] = "same-origin"
        headers["sec-fetch-mode"] = "navigate"
        headers["sec-fetch-user"] = "?1"
        headers["sec-fetch-dest"] = "document"
        headers["accept-language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"
        headers["$cookie"] = "TADCID=XVzfOtYNMUPTPRvCABQCFdpBzzOuRA-9xvCxaMyI12yNOEQ5z7LNoFgE0_ep501H2UlwYtBIt1Iai3qr3SanuQPbd2rhPqkN4Dw; TAUnique=%1%enc%3A8kwUAflygK19OfVULkIYDBus%2FNEwfzUp%2Fi3XVCsbRbH8q3S1%2FtKFWg%3D%3D; TASSK=enc%3AAFK9YnEsKBl1BtTqwxb9XYv1xar2UbPn3NPIl6xk6SZljixK9QJ2zTR7110ehjakPE7ab%2FXb6jtX09WftxdRu8OBGl9cz9G8WMU0G%2B9wGIA4TreJsy3au4fBDMupCOWXoA%3D%3D; ServerPool=X; PMC=V2*MS.5*MD.20220401*LD.20220401; TART=%1%enc%3AfTn1VC5CGAyTSOcLZeWHuo4eFjSKNzs22CFehBRTa2LVMEFUuPIScQB3X0jpqpqmi98diSnNqis%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TASID=EB05A5674D264A1C9346579EFF8337BA; TAReturnTo=%1%%2FRestaurant_Review-g303506-d23085171-Reviews-Coco_Bambu_NorteShopping_Rio-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html; ak_bmsc=ADBD37B10141F7BCC701DF091B43FE04~000000000000000000000000000000~YAAQz9PPF29hwKB/AQAApsN/5w8fH4Z26wU+WpFo4pzNiwtatzg7TDOEx+FlR21/A0aY/crrgB7eTChG8IexQ2Vjscsgzy8AM5fTS+6Wc7N9STU9BU4C158rYnuzF3aFRO4CUlx2qeHKNgbDbzt8pYSsdfxuvc5eblFWJ4iRYIbU0A2kXM76UMWOxXZtqj9AFQfAIKPYlxJ3RxEv4SZfP1P75g20sHqgQdugQVNbXFNRAilyDyXLkzRB5NBQl8+7jOj0C7F03T0I7GkjkzfeAFRgIVJ1dGhO9ok6szamzo43SQzqIQH2Zd4yvIAhnsa2VuqDvs/m5HL8PLHT3T/giLVjEqnCqvMQvLdR/KSvQJ2zpxQCkAjpCCtxvoCxo6BYZrXS32XXjxGAhjqdyM1R4YGkhA==; roybatty=TNI1625u0021ACP6EOgmGMcJuyz%2BpJBVZq1f6G0T%2Fb9DPxT461P0zP9i2RgexwAE36JC9QufvvMxGevJn8TY6gQJPF9H1qp5SHlWnvVIl9F00guTDNcdgusDEXVWm4Bdk8oVoOFUwdIx8Y99sIUQoBlaLYUFRcPqprMqXuw00Dsrgk9FqqSGmcwU%2C1; PAC=AMP6G_wRqdEvRZwZO5z3HZD282ewsZHs7zfX_ebOUTrsF1YEDmms88sHxtRxDYePjCpF2D4zVBK8X0Ssl3jELsX61S-_BjvNCET3F-nh34Ov3XlF7Xp0yksUbMIxH2Kl3pHUw8868iVWtBHSa60f8mf39IwDDg5TGiqNGlM_2q_3RFhMSPezOj-91PBph89iNpAFQdSI78ChjsrD0MQZjbwSoGgibUuwLhg-mvaQoLhtZnFr-f1pJG6P1PjzOL2VlQiEMbZEa4ZhtDbRAh8n-HU%3D; OptanonAlertBoxClosed=2022-04-01T23:40:53.275Z; eupubconsent-v2=CPWy4S1PWy4c1AcABBENCJCsAP_AAH_AACiQIqNf_X__b3_j-_5_f_t0eY1P9_7__-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7_____7z_v-v_v____f_7-3f3__5_3---_e_V_99zbv9____39nP___9v-_9_______BFMAkw1LyALsyxwZNo0qhRAjCsJDqBQAUUAwtEVhA6uCnZXAT6ghYAIBUhOBECDEFGDAIABBIAkIiAkAPBAIgCIBAACABUAhAARsAgsALAwCAAUA0LECKAIQJCDI4IjlMCAqRKKCeysQSg72NMIQyzwIoFH9FQgI1miBYGQkLBzHAEgJeLJA8xQvkAIwAAAAA.f_gAD_gAAAAA; OTAdditionalConsentString=1~39.43.46.55.61.70.83.89.93.108.117.122.124.131.135.136.143.144.147.149.159.162.167.171.192.196.202.211.218.228.230.239.241.259.266.272.286.291.311.317.322.323.326.327.338.367.371.385.389.394.397.407.413.415.424.430.436.440.445.449.453.482.486.491.494.495.501.503.505.522.523.540.550.559.560.568.574.576.584.587.591.733.737.745.780.787.802.803.817.820.821.829.839.864.867.874.899.904.922.931.938.979.981.985.1003.1024.1027.1031.1033.1034.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1127.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1211.1215.1226.1227.1230.1252.1268.1270.1276.1284.1286.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1419.1440.1442.1449.1455.1456.1465.1495.1512.1516.1525.1540.1548.1555.1558.1564.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1665.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1808.1810.1825.1827.1832.1837.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2044.2046.2047.2052.2056.2064.2068.2070.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2202.2205.2216.2219.2220.2222.2225.2234.2253.2264.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2366.2370.2376.2377.2387.2392.2394.2400.2403.2405.2407.2411.2414.2416.2418.2425.2427.2440.2447.2459.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2492.2493.2496.2497.2498.2499.2501.2510.2511.2517.2526.2527.2532.2534.2535.2542.2544.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2595.2596.2601.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2634.2636.2642.2643.2645.2646.2647.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2686.2687.2690.2695.2698.2707.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2818.2821.2822.2827.2830.2831.2834.2836.2838.2839.2840.2844.2846.2847.2849.2850.2851.2852.2854.2856.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2911.2912.2913.2914.2916.2917.2918.2919.2920.2922.2923.2924.2927.2929.2930.2931.2939.2940.2941.2942.2947.2949.2950.2956.2961.2962.2963.2964.2965.2966.2968.2970.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2991.2993.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3045.3048.3052.3053.3055.3058.3059.3063.3065.3066.3068.3070.3072.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3100.3104.3106.3109.3112.3116.3117.3118.3119.3120.3124.3126.3127.3128.3130.3135.3136.3145.3149.3150.3151.3154.3155.3162.3163.3167.3172.3173.3180.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3197.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Apr+01+2022+20%3A40%3A53+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.30.0&isIABGlobal=false&hosts=&consentId=50d92c58-33fd-4959-9b27-5345899a1585&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1; SRT=%1%enc%3AfTn1VC5CGAyTSOcLZeWHuo4eFjSKNzs22CFehBRTa2LVMEFUuPIScQB3X0jpqpqmi98diSnNqis%3D; __vt=Cj3QaUPUkV5I5vl-ABQCIf6-ytF7QiW7ovfhqc-AvRxq9LJwqlCumHvd5uplHHpttuET4uWee-CGIRZUcCq5Z0nu-tKT_-xe4V9zwj5-LdqUkYzPePos1q9eWW3yTT0YbRixHK_mzZNTOYoy9bmHI-5rBw; TASession=V2ID.EB05A5674D264A1C9346579EFF8337BA*SQ.6*LS.DemandLoadAjax*GR.35*TCPAR.80*TBR.92*EXEX.74*ABTR.65*PHTB.13*FS.91*CPU.88*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.pt*FA.1*DF.0*TRA.true*LD.23085171*EAU._; TAUD=LA-1648856388128-1*RDD-1-2022_04_02*LG-1770303-2.1.F.*LD-1770304-.....; bm_sv=C2AB400EA0AE42749B5B07E884731042~B2MkvmiFQg422gxaFw6wmejUtYil6c4JkvdMdyw/Obj6WLwIXRE6zm5+gTvu7LQYusxgV8VgSkHxYeoYh6IrA9yAfg0shti8m4Y8/sUx9oP7z+zdtLNKgG8Rx5y2GOzXxY9efaZDV+E0I2UI2tjtYDPl5N6uDSrav8waEtTIrn8="

        resp = session.get(url, headers=headers)

        # print(session.cookies.get_dict())
        # sys.exit()


        soup = BeautifulSoup(resp.text, 'html.parser')

        nomeEmpresa = soup.find('h1', {"class":"fHibz"}).getText()
        avaliacoes = soup.find('span', {"class":"eBTWs"}).getText().split()[0]
        notaGeral = soup.find('span', {"class":"fdsdx"}).getText().split()[0]

        pontuacaoDosViajantes = soup.find_all('span', {"class":"row_num"})
        breakdownNotas = {
            '5':pontuacaoDosViajantes[0].getText(),
            '4':pontuacaoDosViajantes[1].getText(),
            '3':pontuacaoDosViajantes[2].getText(),
            '2':pontuacaoDosViajantes[3].getText(),
            '1':pontuacaoDosViajantes[4].getText(),
        }
        # pontuacoes => comida | servico | preco
        pontuacoes = soup.find_all('span', {"class":"cwxUN"})
        pontuacaoComida = pontuacoes[0].span['class'][1].split('_')[1]
        pontuacaoServico = pontuacoes[1].span['class'][1].split('_')[1]
        pontuacaoPreco = pontuacoes[2].span['class'][1].split('_')[1]

        ranking = 'Nº ' + soup.find_all('a', {"class":"fhGHT"})[0].getText().split(' ')[1] + ' de ' + soup.find_all('a', {"class":"fhGHT"})[0].getText().split(' ')[3]
        localidadeRanking = soup.find_all('a', {"class":"fhGHT"})[0].getText().split('em')[1].strip()
        endereco = soup.find_all('a', {"class":"fhGHT"})[1].getText()
        cidade = soup.find_all('a', {"class":"fhGHT"})[1].getText().split(',')[2].strip()
        telefone = soup.find_all('a', {"class":"iPqaD"})[1].getText()

        reviews = []

        buscarReviews = True
        mesLimite = MesLimite()
        contadorPag = 0
        idPage = 10
        while(buscarReviews):    
            if contadorPag !=0:
                # "https://www.tripadvisor.com.br/Restaurant_Review-g303506-d23085171-Reviews-or10-Coco_Bambu_NorteShopping_Rio-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html"
                part1 = url.split('-Reviews-')[0]
                part2 = url.split('-Reviews-')[1]
                urlPage = part1 + '-Reviews-or' + str(idPage) +'-'+part2
                idPage += 10

                headers = CaseInsensitiveDict()
                headers["authority"] = "www.tripadvisor.com.br"
                headers["x-puid"] = "f524fca3-7d7d-4085-a053-28bcf52b8bf8"
                headers["sec-ch-ua-mobile"] = "?0"
                headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
                headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                headers["accept"] = "text/html, */*"
                headers["x-requested-with"] = "XMLHttpRequest"
                headers["sec-ch-ua-platform"] = '"Windows"'
                headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
                headers["origin"] = "https://www.tripadvisor.com.br"
                headers["sec-fetch-site"] = "same-origin"
                headers["sec-fetch-mode"] = "cors"
                headers["sec-fetch-dest"] = "empty"
                headers["referer"] = urlPage
                headers["accept-language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"
                headers["$cookie"] = "TADCID=XVzfOtYNMUPTPRvCABQCFdpBzzOuRA-9xvCxaMyI12yNOEQ5z7LNoFgE0_ep501H2UlwYtBIt1Iai3qr3SanuQPbd2rhPqkN4Dw; TAUnique=%1%enc%3A8kwUAflygK19OfVULkIYDBus%2FNEwfzUp%2Fi3XVCsbRbH8q3S1%2FtKFWg%3D%3D; TASSK=enc%3AAFK9YnEsKBl1BtTqwxb9XYv1xar2UbPn3NPIl6xk6SZljixK9QJ2zTR7110ehjakPE7ab%2FXb6jtX09WftxdRu8OBGl9cz9G8WMU0G%2B9wGIA4TreJsy3au4fBDMupCOWXoA%3D%3D; TART=%1%enc%3AfTn1VC5CGAyTSOcLZeWHuo4eFjSKNzs22CFehBRTa2LVMEFUuPIScQB3X0jpqpqmi98diSnNqis%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; OptanonAlertBoxClosed=2022-04-01T23:40:53.275Z; eupubconsent-v2=CPWy4S1PWy4c1AcABBENCJCsAP_AAH_AACiQIqNf_X__b3_j-_5_f_t0eY1P9_7__-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7_____7z_v-v_v____f_7-3f3__5_3---_e_V_99zbv9____39nP___9v-_9_______BFMAkw1LyALsyxwZNo0qhRAjCsJDqBQAUUAwtEVhA6uCnZXAT6ghYAIBUhOBECDEFGDAIABBIAkIiAkAPBAIgCIBAACABUAhAARsAgsALAwCAAUA0LECKAIQJCDI4IjlMCAqRKKCeysQSg72NMIQyzwIoFH9FQgI1miBYGQkLBzHAEgJeLJA8xQvkAIwAAAAA.f_gAD_gAAAAA; OTAdditionalConsentString=1~39.43.46.55.61.70.83.89.93.108.117.122.124.131.135.136.143.144.147.149.159.162.167.171.192.196.202.211.218.228.230.239.241.259.266.272.286.291.311.317.322.323.326.327.338.367.371.385.389.394.397.407.413.415.424.430.436.440.445.449.453.482.486.491.494.495.501.503.505.522.523.540.550.559.560.568.574.576.584.587.591.733.737.745.780.787.802.803.817.820.821.829.839.864.867.874.899.904.922.931.938.979.981.985.1003.1024.1027.1031.1033.1034.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1127.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1211.1215.1226.1227.1230.1252.1268.1270.1276.1284.1286.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1419.1440.1442.1449.1455.1456.1465.1495.1512.1516.1525.1540.1548.1555.1558.1564.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1665.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1808.1810.1825.1827.1832.1837.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2044.2046.2047.2052.2056.2064.2068.2070.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2202.2205.2216.2219.2220.2222.2225.2234.2253.2264.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2366.2370.2376.2377.2387.2392.2394.2400.2403.2405.2407.2411.2414.2416.2418.2425.2427.2440.2447.2459.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2492.2493.2496.2497.2498.2499.2501.2510.2511.2517.2526.2527.2532.2534.2535.2542.2544.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2595.2596.2601.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2634.2636.2642.2643.2645.2646.2647.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2686.2687.2690.2695.2698.2707.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2818.2821.2822.2827.2830.2831.2834.2836.2838.2839.2840.2844.2846.2847.2849.2850.2851.2852.2854.2856.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2911.2912.2913.2914.2916.2917.2918.2919.2920.2922.2923.2924.2927.2929.2930.2931.2939.2940.2941.2942.2947.2949.2950.2956.2961.2962.2963.2964.2965.2966.2968.2970.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2991.2993.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3045.3048.3052.3053.3055.3058.3059.3063.3065.3066.3068.3070.3072.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3100.3104.3106.3109.3112.3116.3117.3118.3119.3120.3124.3126.3127.3128.3130.3135.3136.3145.3149.3150.3151.3154.3155.3162.3163.3167.3172.3173.3180.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3197.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; PAC=AEoqpZoeqYuxHAvNRpGqsk-XQn7ySDelGsr01u7JoRhsmmit_x1Zzj5mMQSl5jBvBrFlBCUEr8QvltzGUCV69sgRoMx8DlgNc9HXfZU6GT_Gy_EWV-hyRjCUwgPOF2F8Ijb65fh3mreMU7VzLMcC2uXqNpykf8BBAdOwGHcKlBUCSLptfQ5ZIes8J4piw0aSdz0kuMEcE_pRHtyaCIbJlM_xB6zYDCk1XApa5USi3GIpoyVfagn6UZmDPCMw5yp6J2AVldhbHMtOY8-p8GDk4Kc%3D; ServerPool=B; PMC=V2*MS.5*MD.20220401*LD.20220402; TASID=CF173FC91388458C8119370E57CDE850; ak_bmsc=DB0FFD8B2C45706041F786EDCCD26320~000000000000000000000000000000~YAAQR9hHaK+kM79/AQAA3Mio6g8kpYiFqpWBHU2Vot18mSeLTUQKegZI2EcImu3W2Dx7VYoBzDK5Q1U2v0W+BwyjbxhpIZB8sf/NrKPPEwzPLDRGw3Daw4kxJt4hu9EGgSf6Uiw4/FcZD6w2EuDRnBYoshL/W63JrOX965qlGWyPjSY0rJzfHcj49EOqu/6AiWDG1f2rLVpUDz1ubOfpy8TxDv2aVaiHBKzDZbjehnGW+mhhTSfhKOfrLZhb9pmRoLMGPKf6r4kN1GbTyoyU1u1SvwJ9tQMIJc3m4/vEecWjjhTanVe6F81e0nrTZ9d5RBsfzJ0wpDJ0dzBwfhEUvgpGdi6H+cuxE+LHWZiZoYON6CrUq8oknprgsNuQDFANx6FtI14y4L+nzGUqXzX5QFeWjQ==; roybatty=TNI1625u0021APwFrYxPA01vKdNxsQBcdXVZFzQepM8rH%2FQRee2xRTSsf1jYNYt5G3roswxPB9rpC8EZtzC7W4i3%2B95mQQExpqbMU41G6xJONljeyMF7%2FgR0OOX%2BFPcQx75U0ig6KejuSwXlzdwyGqdVEydIWqEBkYbsTH36w54Y9bmnFhMfLEb2%2C1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+02+2022+11%3A23%3A34+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.30.0&isIABGlobal=false&hosts=&consentId=50d92c58-33fd-4959-9b27-5345899a1585&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=BR%3BMG&AwaitingReconsent=false; TASession=V2ID.CF173FC91388458C8119370E57CDE850*SQ.13*LS.MetaPlacementAjax*GR.44*TCPAR.64*TBR.10*EXEX.66*ABTR.63*PHTB.48*FS.48*CPU.42*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.pt*FA.1*DF.0*TRA.true*LD.23085171*EAU._; TAUD=LA-1648856388128-1*RDD-1-2022_04_02*LG-53674983-2.1.F.*LD-53674984-.....; TAReturnTo=%1%%2FRestaurant_Review%3Fg%3D303506%26reqNum%3D1%26puid%3Df524fca3-7d7d-4085-a053-28bcf52b8bf8%26isLastPoll%3Dfalse%26d%3D23085171%26waitTime%3D40%26paramSeqId%3D0%26changeSet%3DREVIEW_LIST; __vt=ZIT4LHMuNcT9WYbRABQCIf6-ytF7QiW7ovfhqc-AvRxuiHgLQKAw2sw-yznuWte0_LMB-Ug38G-X0ngtUapDOzQMEbQ7-zi_ppP3wgrSa_ma14JHWC4LEUOLkTFUAbZL68IYzlgm_qB1bEIvnnGfbKzfSA; bm_sv=4A1D88FBEF98B0927E5EBCD6A9044A38~wTpPLGW3+um1Nv4y/N/dwDIJMMipN3dk/QNh8XgUOPLL3ve/kyVX8Ind5/WseVEzHWJyFHnELQRWPtYeOmWjG9VkYTLcvfloZ/P6NTRSLzFMpfvKM+l6wQvp7wgUsOdjXcu8mhMwF7CvZ6P7giTpa57uw/sNlYmrZHCK+oHBm6w="

                data = {
                    'reqNum':'1',
                    'isLastPoll':'false',
                    'paramSeqId':'0',
                    'waitTime': random.randint(15,38),
                    'changeSet':'REVIEW_LIST',
                    'puid':'f524fca3-7d7d-4085-a053-28bcf52b8bf8'
                }
                resp = session.post(urlPage, headers=headers, data=data)
                soup = BeautifulSoup(resp.text, 'html.parser')

            divReviews = soup.find_all('div', {'class':'review-container'})

            for div in divReviews:
                dataReview = div.find('div',{'data-prwidget-name':'reviews_stay_date_hsx'}).getText().split(':')[1].strip()
                review = div.find('div',{'class':'entry'}).getText()
                nota = div.find_all('span')[1]['class'][1].split('bubble_')[1]
                
                if(dataReview.split(' ')[0] == mesLimite):
                    buscarReviews = False
                    break

                reviews.append({
                    'local': nomeEmpresa,
                    'review':review,
                    'nota': nota,
                    'dataReview': dataReview,
                    'cidadeLocal': cidade
                })

            contadorPag+=1

        dados = {
            'notas': {
                'nome': nomeEmpresa,
                'numeroAvaliacoes': avaliacoes,
                'notaGeral': notaGeral,
                'breakdownNotas': breakdownNotas,
                'pontuacaoComida': pontuacaoComida,
                'pontuacaoServico': pontuacaoServico,
                'pontuacaoPreco': pontuacaoPreco,
                'ranking': ranking,
                'localidadeRanking': localidadeRanking,
                'cidade': cidade,
                'endereco': endereco,
                'telefone': telefone
            },
            'reviews': reviews
        }
        print(json.dumps(dados))
    except Exception as ex:
        print(ex)

