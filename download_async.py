""" This script will download the async data from the google sheets and format it appropriately """
import sys
import os
import requests
import datetime as dt


class RaceEntrant():
    def __init__(self, sheet_row):
        sheet_row = sheet_row.split(',')
        self.timestamp1 = sheet_row[0]
        self.display_name = sheet_row[1].split('#')[0].strip()
        self.rturl = sheet_row[3].strip()

        self.tdelta = None
        self.finish_time = None
        self.placement = None

    def include_responses(self, resp):
        thisrow = None
        for row in resp:
            if row[9].strip() == self.rturl:
                thisrow = row
                break

        if thisrow is not None:
            self.timestamp2 = thisrow[0]
            ftime = thisrow[6].strip().split(':')
            if len(ftime) == 1: # This is the case where they write something like `forfeit` into the time field
                self.finish_time = None
            elif len(ftime) == 2: # If time is under an hour
                self.finish_time = dt.timedelta(minutes=float(ftime[0]), seconds=round(float(ftime[1])))
            else:
                self.finish_time = dt.timedelta(hours=float(ftime[0]), minutes=float(ftime[1]), seconds=round(float(ftime[2])))


    def build_output_row(self):
        if self.placement is None:
            output = [self.rturl, 'null', self.display_name, 'dnf', 'null']
        else:
            prettytime = 'P0DT' + \
                str(self.finish_time.seconds//3600) + 'H' + \
                str((self.finish_time.seconds//60)%60) + 'M' + \
                str(self.finish_time.seconds%60) +'S'
            output = [self.rturl, self.placement, self.display_name, 'done', prettytime]

        return ','.join([str(x) for x in output]) + '\n'


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
        {"name": "responses", "doc_id": "1rqBlRU3GayPKWjja76A_7bavWdTveVSEjw-JK5o2cQY", "tab_id": "623017156"}
    ]
    for sheet in sheet_list:
        response = requests.get(f"https://docs.google.com/spreadsheets/d/{sheet['doc_id']}/export?format=csv&gid={sheet['tab_id']}")
        with open(f"google_sheets/{sheet['name']}.csv", 'w') as fp:
            fp.write(response.text)

    # Change this to keep the files in memory rather than save and reopen
    with open('google_sheets/requests.csv', 'r') as fin:
        req = fin.readlines()[1:]
        req = [line.strip() for line in req]
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
    with open(f"other_races/rated_async_{asyn_number}.txt", 'w') as fp:
        fp.write(f"Rated Async {asyn_number}\n")
        fp.write(f"rated_async_{asyn_number}\n")
        fp.write("2020-<MM>-<DD>T04:00:00Z\n")
        for entr in entrants:
            fp.write(entr.build_output_row())
        




if __name__ == "__main__":
    main()