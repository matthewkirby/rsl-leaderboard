# I can link to racetime using player.userid


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
    return f"<a href={url}>{player.display_name}</a>"


def generate_html(leaderboard):
    with open("public/index.html", 'w') as fp:
        # Write the preamble
        fp.write("<html>\n<head>\n<title>Rando Rando Leaderboard</title>\n")
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\">\n")
        fp.write("</head>\n<body>\n")

        # Write the body
        fp.write("<main>")
        fp.write("\t<ol>\n")

        # Write the header
        fp.write("\t\t<span class=\"table-header\"><h4>Rando Rando Season 2</h4></span>\n")

        # Write the leaderboard
        for player, place in zip(leaderboard, range(len(leaderboard))):
            fp.write(f"\t\t<li>\n")
            fp.write(f"\t\t\t<span class=\"placement\">{pretty_placement(int(1+place))}</span>\n")
            fp.write(f"\t\t\t<span class=\"player-name\">{name_with_link(player)}</span>\n")
            fp.write(f"\t\t\t<span class=\"rating\">{player.display_rating}</span>\n")
            fp.write(f"\t\t\t<span class=\"race-deetz\">")
            fp.write(f"\t\t\t\t<span class=\"finishes\">{should_i_plural('Finish', int(player.finishes))}</span>\n")
            fp.write(f"\t\t\t\t<span class=\"race-count\">{should_i_plural('Race', int(player.forfeits+player.finishes))}</span>\n")
            fp.write(f"\t\t\t</span>")
            fp.write(f"\t\t</li>\n")
        fp.write("\t</ol>\n")
        fp.write("</main>")

        # Close out tags
        fp.write("</body>\n</html>")