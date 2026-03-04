import requests

url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": "polar bears",
    "limit": 5,
    "fields": "paperId,title,abstract,authors,year,citationCount,venue,url"
}
resp = requests.get(url, params=params)
print("Status:", resp.status_code)
if resp.status_code == 200:
    print("Results:", len(resp.json().get("data", [])))
else:
    print(resp.text)
