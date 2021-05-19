import trueskill
import tools
import json

class Race:
    def __init__(self, filepath, asyn=False):
        if asyn:
            self.init_asyn(filepath)
        else:
            self.init_racetime(filepath)

        self.tabledata = []
        self.htmltable = ""


    def init_racetime(self, filepath):
        """ Initalize a race using data scraped from racetime api """
        with open(filepath, 'r') as fin:
            data = json.load(fin)

        self.slug = data['slug']
        self.race_materials_name = None
        self.datetime = data["ended_at"]
        self.entrants = [{
                "userid": entr['user']['id'],
                "place": entr['place'],
                "display_name": entr['user']['name'],
                "status": entr['status']['value'],
                "finish_time": entr['finish_time']
            } for entr in data['entrants']]
        self.on_racetime = True


    def init_asyn(self, filepath):
        print(filepath)
        with open(filepath, 'r') as fin:
            data = fin.readlines()
        data = [line.strip() for line in data]

        self.slug = data[0]
        self.race_materials_name = data[1]
        self.datetime = data[2]
        self.entrants = [{
                "userid": row.split(',')[0].split('/')[-1],
                "place": int(row.split(',')[1]) if row.split(',')[1] != 'null' else None,
                "display_name": row.split(',')[2],
                "status": row.split(',')[3],
                "finish_time": row.split(',')[4]
            } for row in data[3:]]
        
        for entr in self.entrants:
            if entr['finish_time'] == 'null':
                entr['finish_time'] = None
        self.on_racetime = False

    def build_html(self):
        self.htmltable += "<ol class=\"player-table\">"
        self.htmltable += "<span class=\"table-header\">"
        self.htmltable += f"<h4>{tools.slug_with_link(self.slug, self.on_racetime)}</h4>"
        if self.race_materials_name is not None:
            self.htmltable += "<span class=\"race-materials\">"
            self.htmltable += f"(<a href=\"/race_materials/{self.race_materials_name}_patch.zpf\" class=\"materials\" download>Download Patch</a>) "
            self.htmltable += f"(<a href=\"/race_materials/{self.race_materials_name}_spoiler.json\" class=\"materials\" download>Download Spoiler</a>)"
            self.htmltable += "</span>"
        if self.on_racetime:
            self.htmltable += f"<span class=\"race-date\">{tools.pretty_race_date(self.datetime)}</span>"
            self.htmltable += f"</span><span class=\"placement-block\" style=\"display: block;\">"
        else:
            self.htmltable += "<button class=\"reveal-button\" onclick=\"revealTimes(this)\">Toggle Times</button>"
            self.htmltable += f"</span><span class=\"placement-block hidden\">"
        for player in self.tabledata:
            self.htmltable += "<li class=\"table\">"
            self.htmltable += f"<span class=\"placement\">{tools.pretty_placement(player['place'])}</span>"
            self.htmltable += f"<span class=\"player-name-race\">{player['name']}</span>"
            self.htmltable += f"<span class=\"finish-time\">{tools.pretty_finish_time(player['finish_time'])}</span>"
            self.htmltable += f"<span class=\"rating-delta\">{tools.format_delta(player['delta'])}</span>"
            self.htmltable += "</li>"
        self.htmltable += "</span></ol>"


    def build_table(self, playerlist, placement, start_ratings, end_ratings):
        """ Build dict to display race in webpage. """
        for i in range(len(playerlist)):
            pid = playerlist[i].id
            entr = [x for x in self.entrants if x['userid'] == pid][0]

            # If ff, overwrite placement
            if entr['status'] == 'dnf':
                placement[i] = None

            srate = start_ratings[i][0]
            erate = end_ratings[i][0]
            self.tabledata.append(
                {
                    "place": placement[i],
                    "name": playerlist[i].display_name,
                    "finish_time": entr["finish_time"],
                    "rating": round((erate.mu - 2.*erate.sigma) * 100.),
                    "delta": round((erate.mu - 2.*erate.sigma) * 100.) - round((srate.mu - 2.*srate.sigma) * 100.)
                }
            )
        self.build_html()


    def rate(self, playerlist, placement):
        """ Given a list of players and race placement, compute ratings using trueskill 
        
        Parameters
        ----------
        playerlist: list(Player)
        placement: list(int)
        """
        start_ratings = [(player.rating,) for player in playerlist]
        end_ratings = trueskill.rate(start_ratings, ranks=placement)
        for i in range(len(end_ratings)):
            playerlist[i].rating = end_ratings[i][0]
            playerlist[i].compute_display_rating()
        self.build_table(playerlist, placement, start_ratings, end_ratings)
