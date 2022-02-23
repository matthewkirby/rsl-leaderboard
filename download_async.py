""" This script will download the async data from the google sheets and format it appropriately """
import sys
import os
import requests
import datetime as dt


patreon_conversion = {
    "emosoda": "07QXz83Ke6WeZDjr",
    "rando-god": "PyZ2Dv30Q4oewXma",
    "BrotinderDose": "NY0OkW1Y2vWKalP1"
}


class RaceEntrant():
    def __init__(self, sheet_row):
        self.timestamp1 = sheet_row[0]
        self.display_name = sheet_row[1].split('#')[0].strip()
        self.rturl = sheet_row[3].strip()

        self.tdelta = None
        self.finish_time = None
        self.placement = None

    def include_responses(self, resp):
        # Find the row in responses that matches the entrant
        thisrow = None
        for row in resp:
            if row[2].strip() == self.rturl:
                thisrow = row
                break

        # If a reponse was found, match things
        if thisrow is not None:
            self.timestamp2 = thisrow[0]
            ftime = thisrow[4].strip()
            # Account for forfeits that fill out the form
            if ftime in ['0:00:00', '69:59:59']:
                return
            self.finish_time = dt.timedelta(
                hours=float(ftime.split(':')[0]),
                minutes=float(ftime.split(':')[1]),
                seconds=round(float(ftime.split(':')[2])))


    def build_output_row(self):
        # Replace patreon vanity URLs
        userid = self.rturl.split("https://racetime.gg/user/")[1]
        if userid in patreon_conversion:
            userid = patreon_conversion[userid]
        self.rturl = "https://racetime.gg/user/" + userid

        # Write the line for output
        if self.placement is None:
            output = [self.rturl, 'null', self.display_name, 'dnf', 'null']
        else:
            prettytime = 'P0DT' + \
                str(self.finish_time.seconds//3600) + 'H' + \
                str((self.finish_time.seconds//60)%60) + 'M' + \
                str(self.finish_time.seconds%60) +'S'
            output = [self.rturl, self.placement, self.display_name, 'done', prettytime]

        return ','.join([str(x) for x in output]) + '\n'


def download_asyncs(sheet_list):
    for sheet in sheet_list:
        response = requests.get(f"https://docs.google.com/spreadsheets/d/{sheet['doc_id']}/export?format=csv&gid={sheet['tab_id']}")
        with open(f"google_sheets/{sheet['name']}.csv", 'w') as fp:
            fp.write(response.text)


def main():
    # Ensure that the files for the given async do not already exist
    asyn_number = int(sys.argv[1])
    if os.path.exists(f"other_races/rated_async_{asyn_number}.txt"):
        print(f"Race data for rated async {asyn_number} already exists...\nExiting...")
        sys.exit(1)
    print(f"Downloading data for async number {asyn_number}")

    # Download the google sheets
    sheet_list = [
        {"name": "requests", "doc_id": "1RGPpMSdsQZtmROEqIsrN_5Nt8Z0RfKZ2EeW-DFj9uus", "tab_id": "133854036"},
        {"name": "responses", "doc_id": "1D-QGG-reSHuVzSQP6tzEW_s-TjkNgouIF7U80mNjoJo", "tab_id": "1877272115"}
    ]
    download_asyncs(sheet_list)

    # Change this to keep the files in memory rather than save and reopen
    with open('google_sheets/requests.csv', 'r') as fin:
        req = fin.readlines()[1:]
        req = [line.strip().split(',') for line in req]
    with open('google_sheets/responses.csv', 'r') as fin:
        resp = fin.readlines()[1:]
        resp = [line.strip().split(',') for line in resp]

    # Put all of the runners into a list based on requests and match responses
    entrants = [RaceEntrant(row) for row in req]
    for entr in entrants:
        entr.include_responses(resp)

    # Sort the runners by time and apply a ranking
    entrants.sort(key=lambda entr: entr.finish_time if entr.finish_time is not None else dt.timedelta(days=7))
    for i in range(len(entrants)):
        if entrants[i].finish_time is not None:
            entrants[i].placement = i+1

    # Write output file
    today = dt.date.today()
    with open(f"other_races/rated_async_{asyn_number}.txt", 'w') as fp:
        fp.write(f"Rated Async {asyn_number}\n")
        fp.write(f"rated_async_{asyn_number}\n")
        fp.write(f"2022-{today.month:02d}-{today.day:02d}T04:00:00Z\n")
        for entr in entrants:
            fp.write(entr.build_output_row())
        




if __name__ == "__main__":
    main()