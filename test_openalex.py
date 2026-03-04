import requests

url = "https://api.openalex.org/works"
params = {
    "search": "polar bears",
    "per_page": 5,
}
resp = requests.get(url, params=params)
print("Status:", resp.status_code)
if resp.status_code == 200:
    data = resp.json().get("results", [])
    print("Results:", len(data))
    if data:
        print("First title:", data[0].get("title"))
else:
    print(resp.text)
