import os
import requests
import time
import json
import certifi

TOKEN = "xxxxxx"

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
OUT_JSON = "java_repos_1000.json"
OUT_LIST = "java_repos_list.txt"


def fetch_page(q, page, per_page=100):
    url = "https://api.github.com/search/repositories"
    params = {"q": q, "sort": "stars", "order": "desc", "per_page": per_page, "page": page}
    r = requests.get(url, headers=HEADERS, params=params, verify=certifi.where())
    r.raise_for_status()
    return r.json()

def main():
    query = "language:Java"
    per_page = 100
    max_pages = 10  
    all_items = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        data = fetch_page(query, page, per_page=per_page)
        items = data.get("items", [])
        if not items:
            break
        all_items.extend(items)
        time.sleep(1)
    all_items = all_items[:1000]
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    with open(OUT_LIST, "w", encoding="utf-8") as f:
        for it in all_items:
            f.write(f"{it['full_name']}\n")
    print(f"Wrote {len(all_items)} repos to {OUT_JSON} and {OUT_LIST}")

if __name__ == "__main__":
    main()
