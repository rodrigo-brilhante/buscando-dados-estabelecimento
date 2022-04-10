import requests
from requests.structures import CaseInsensitiveDict

url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/coc"

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

print(resp.text)

