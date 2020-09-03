
def pretty_placement(i):
    if i == 1:
        return "<div class=\"first-place\">1st</div>"
    elif i == 2:
        return "<div class=\"second-place\">2nd</div>"
    elif i == 3:
        return "<div class=\"third-place\">3rd</div>"
    else:
        return f"{i}th"

def should_i_plural(string, i):
    if string == 'Finish':
        return f"{i} {string}" if i == 1 else f"{i} {string}es"
    elif string == 'Race':
        return f"{i} {string}" if i == 1 else f"{i} {string}s"


def name_with_link(player):
    url = f"https://racetime.gg/user/{player.id}"
    return f"<a href={url} class=\"a-table\">{player.display_name}</a>"


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
        fp.write("<li class=\"li-header\"><a href=\"\\\" class=\"a-header\">Race List</a></li>")
        fp.write("\t</ul>")
        fp.write("</header>\n")


        # Write the body
        fp.write("<main>\n")
        fp.write("\t<ol class=\"ol-table\">\n")

        # Write the header
        fp.write("\t\t<span class=\"table-header\"><h4>Rando Rando Season 2</h4></span>\n")

        # Write the leaderboard
        for player, place in zip(leaderboard, range(len(leaderboard))):
            fp.write(f"\t\t<li class=\"li-table\">\n")
            fp.write(f"\t\t\t<span class=\"placement\">{pretty_placement(int(1+place))}</span>\n")
            fp.write(f"\t\t\t<span class=\"player-name\">{name_with_link(player)}</span>\n")
            fp.write(f"\t\t\t<span class=\"rating\">{player.display_rating}</span>\n")
            fp.write(f"\t\t\t<span class=\"race-deetz\">\n")
            fp.write(f"\t\t\t\t<span class=\"finishes\">{should_i_plural('Finish', int(player.finishes))}</span>\n")
            fp.write(f"\t\t\t\t<span class=\"race-count\">{should_i_plural('Race', int(player.forfeits+player.finishes))}</span>\n")
            fp.write(f"\t\t\t</span>\n")
            fp.write(f"\t\t</li>\n")
        fp.write("\t</ol>\n")
        fp.write("</main>\n")

        # Close out tags
        fp.write("</body>\n</html>")