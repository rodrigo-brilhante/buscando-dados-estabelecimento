import requests
from requests.structures import CaseInsensitiveDict
import requests
from requests.structures import CaseInsensitiveDict

query='coco bambu'.replace(' ', '+')
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

print(resp.text)

