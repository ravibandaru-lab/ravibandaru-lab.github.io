import json
import time
import urllib.request
import urllib.error

PAPERS_PATH = "papers.json"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=citationCount"

with open(PAPERS_PATH) as f:
    papers = json.load(f)

updated = False

for paper in papers:
    doi = paper.get("doi")
    if not doi:
        continue

    url = S2_API.format(doi=doi)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            count = data.get("citationCount")
            if count is not None and count != paper.get("citations"):
                print(f"Updated '{paper['title'][:60]}...' : {paper.get('citations')} -> {count}")
                paper["citations"] = count
                updated = True
            else:
                print(f"No change for '{paper['title'][:60]}...' ({count} citations)")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for DOI {doi} — skipping")
    except Exception as e:
        print(f"Error for DOI {doi}: {e} — skipping")

    time.sleep(1)  # be polite to the API

if updated:
    with open(PAPERS_PATH, "w") as f:
        json.dump(papers, f, indent=2)
    print("papers.json updated.")
else:
    print("No changes to papers.json.")
