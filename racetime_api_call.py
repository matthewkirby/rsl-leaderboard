import requests
import json
import os
import dateutil.parser

SEASON_START_DATE = dateutil.parser.parse("2021-09-15T00:0:0.000Z")

def download_sluglist():
    sluglist = []
    with open("races/last_race_seen.txt", 'r') as fp:
        last_race = fp.read()

    # Download the race history
    racelist = []
    for page_num in range(20):
        if page_num == 19:
            raise Exception("Went 20 pages and did not find the last seen race.")
        onepage = requests.get(f"https://racetime.gg/ootr/races/data?page={page_num+1}").json()['races']
        racelist += onepage
        if last_race in [onerace["name"] for onerace in onepage]:
            break
        
    # Identify RSL League races
    for race in racelist:
        if race["name"] == last_race:
            break
        if race["goal"]["name"] == "Random settings league":
            if race["info"].startswith("Random Settings League | Seed: "):
                sluglist.append(race["name"].split("/")[1])

    # Write the slug of the most recent race
    with open("races/last_race_seen.txt", 'w') as fp:
        fp.write(racelist[0]["name"])

    if len(sluglist) > 0:
        print(f"Found {len(sluglist)} new races!")
    return sluglist


def fetch_race(slug):
    outpath = f"races/{slug}.json"
    if os.path.exists(outpath):
        return

    print(f"Fetching race data for {slug}.")
    response = requests.get(f"https://racetime.gg/ootr/{slug}/data")
    with open(outpath, 'w') as fp:
        json.dump(response.json(), fp, indent=4)