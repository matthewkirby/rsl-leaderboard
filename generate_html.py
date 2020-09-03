import tools

def generate_website(leaderboard, racelist):
    generate_html_leaderboard(leaderboard)
    generate_html_racelist(racelist)
    generate_resources()


def generate_html_leaderboard(leaderboard):
    with open("public/index.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html") as fin:
            header = fin.read()
        fp.write(header)

        # Write the leaderboard
        fp.write("\t<ol class=\"ol-table\">\n")
        fp.write("\t\t<span class=\"table-header\"><h4>Rando Rando Season 2</h4></span>\n")
        for player, place in zip(leaderboard, range(len(leaderboard))):
            fp.write(f"\t\t<li class=\"li-table\">\n")
            fp.write(f"\t\t\t<span class=\"placement\">{tools.pretty_placement(int(1+place))}</span>\n")
            fp.write(f"\t\t\t<span class=\"player-name\">{tools.name_with_link(player)}</span>\n")
            fp.write(f"\t\t\t<span class=\"rating\">{player.display_rating}</span>\n")
            fp.write(f"\t\t\t<span class=\"race-deetz\">\n")
            fp.write(f"\t\t\t\t<span class=\"finishes\">{tools.should_i_plural('Finish', int(player.finishes))}</span>\n")
            fp.write(f"\t\t\t\t<span class=\"race-count\">{tools.should_i_plural('Race', int(player.forfeits+player.finishes))}</span>\n")
            fp.write(f"\t\t\t</span>\n")
            fp.write(f"\t\t</li>\n")
        fp.write("\t</ol>\n")

        # Close out tags
        with open("html_templates/closeout.html") as fin:
            footer = fin.read()
        fp.write(footer)

def generate_html_racelist(racelist):
    with open("public/racelist.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            header = fin.read()
        fp.write(header)

        # Write the body
        for race in racelist[::-1]:
            fp.write(race.htmltable)
            fp.write("</p>")

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            footer = fin.read()
        fp.write(footer)

def generate_resources():
    with open("public/resources.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            header = fin.read()
        fp.write(header)

        # Write the body
        with open("html_templates/resource_body.html", 'r') as fin:
            body = fin.read()
        fp.write(body)

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            footer = fin.read()
        fp.write(footer)