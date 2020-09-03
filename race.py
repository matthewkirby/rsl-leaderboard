import trueskill
import tools
import json

class Race:
    def __init__(self, filepath):
        with open(filepath, 'r') as fin:
            data = json.load(fin)

        self.slug = data['slug']
        self.datetime = data["ended_at"]
        self.entrants = [{
                "userid": entr['user']['id'],
                "place": entr['place'],
                "display_name": entr['user']['name']
            } for entr in data['entrants']]
        self.tabledata = []
        self.htmltable = ""


    def build_html(self):
        self.htmltable += "\t<ol class=\"ol-table\">\n"
        self.htmltable += f"\t\t<span class=\"table-header\"><h4>{tools.slug_with_link(self.slug)}</h4></span>\n"
        for player in self.tabledata:
            self.htmltable += "\t\t<li class=\"li-table\">\n"
            self.htmltable += f"\t\t\t<span class=\"placement\">{tools.pretty_placement(int(player['place']))}</span>\n"
            self.htmltable += f"\t\t\t<span class=\"player-name\">{player['name']}</span>\n"
            self.htmltable += f"\t\t\t<span class=\"rating\">{player['rating']}</span>\n"
            self.htmltable += f"\t\t\t<span class=\"rating-delta\">{tools.format_delta(player['delta'])}</span>\n"
            self.htmltable += "\t\t</li>\n"
        self.htmltable += "\t</ol>\n"


    def build_table(self, playerlist, placement, start_ratings, end_ratings):
        """ Build dict to display race in webpage. """
        for i in range(len(playerlist)):
            srate = start_ratings[i][0]
            erate = end_ratings[i][0]
            self.tabledata.append(
                {
                    "place": placement[i],
                    "name": playerlist[i].display_name,
                    "rating": round((srate.mu - 2.*srate.sigma) * 100.),
                    "delta": round((erate.mu - 2.*erate.sigma) * 100.) - round((srate.mu - 2.*srate.sigma) * 100.)
                }
            )
        self.build_html()


    def rate(self, playerlist, placement):
        """ Given a list of players and race placement, compute ratings using trueskill """
        start_ratings = [(player.rating,) for player in playerlist]
        end_ratings = trueskill.rate(start_ratings, ranks=placement)
        for i in range(len(end_ratings)):
            playerlist[i].rating = end_ratings[i][0]
            playerlist[i].compute_display_rating()
        self.build_table(playerlist, placement, start_ratings, end_ratings)
