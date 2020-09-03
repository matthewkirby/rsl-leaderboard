import tools

def generate_html_leaderboard(leaderboard):
    with open("public/index.html", 'w') as fp:
        # Write the preamble
        fp.write("<html>\n<head>\n<title>Rando Rando Leaderboard</title>\n")
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\">\n")
        fp.write("</head>\n<body>\n")

        # Write the header
        fp.write("<header>\n")
        fp.write("\t<ul class=\"ul-header\">")
        fp.write("<li class=\"li-header\"><a href=\"\\\" class=\"a-header\">Leaderboard</a></li>")
        fp.write("<li class=\"li-header\"><a href=\"racelist\" class=\"a-header\">Race List</a></li>")
        fp.write("\t</ul>")
        fp.write("</header>\n")


        # Write the body
        fp.write("<main>\n")
        fp.write("<div class\"contain-table\">")
        fp.write("\t<ol class=\"ol-table\">\n")

        # Write the header
        fp.write("\t\t<span class=\"table-header\"><h4>Rando Rando Season 2</h4></span>\n")

        # Write the leaderboard
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
        fp.write("\t</ol>\n</div>")
        fp.write("</main>\n")

        # Close out tags
        fp.write("</body>\n</html>")


def generate_html_racelist(racelist):
    with open("public/racelist.html", 'w') as fp:
        # Write the preamble
        fp.write("<html>\n<head>\n<title>Rando Rando Season 2 Races</title>\n")
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\">\n")
        fp.write("</head>\n<body>\n")

        # Write the header
        fp.write("<header>\n")
        fp.write("\t<ul class=\"ul-header\">")
        fp.write("<li class=\"li-header\"><a href=\"\\\" class=\"a-header\">Leaderboard</a></li>")
        fp.write("<li class=\"li-header\"><a href=\"racelist\" class=\"a-header\">Race List</a></li>")
        fp.write("\t</ul>")
        fp.write("</header>\n")


        # Write the body
        fp.write("<main>\n")
        for race in racelist[::-1]:
            fp.write(race.htmltable)
            fp.write("</p>")
        fp.write("</main>\n")

        # Close out tags
        fp.write("</body>\n</html>") 
