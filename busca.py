import undetected_chromedriver as uc
from selenium import webdriver
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import warnings
warnings.filterwarnings('ignore')

def click(driver, selector):
    try:
        element = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    except:
        pass
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.double_click(element)
    actions.perform()



# options = webdriver.ChromeOptions() 
# options.add_argument("start-maximized")
# # options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = uc.Chrome(options=options)

# print('iniciando...')
# driver.get('https://www.tripadvisor.com.br/Search?q=coco%20bambu%20bahia')
import requests
from requests.structures import CaseInsensitiveDict

query="coco bambu"
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
for result in results:
    try:
        if 'Todos os resultados para' not in result['name']:
            if result['name'] and result['address']:
                print(result)
    except:
        pass
