import requests
import json
import os

def fetch_race(slug):
    outpath = f"races/{slug}.json"
    if os.path.exists(outpath):
        # print(f"Skipping {slug}.")
        return

    print(f"Fetching race data for {slug}.")
    response = requests.get(f"https://racetime.gg/ootr/{slug}/data")
    with open(outpath, 'w') as fp:
        json.dump(response.json(), fp, indent=4)