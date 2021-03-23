import tools
import weights
import re

def generate_website(leaderboard, unqualed, racelist):
    generate_html_leaderboard(leaderboard, unqualed)
    generate_html_racelist(racelist)
    generated_rated_asyncs(racelist)
    generate_html_weights()
    generate_resources()


def generate_html_leaderboard(leaderboard, unqualed):
    with open("public/index.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html") as fin:
            header = fin.read()
        fp.write(header)

        # Write the hash block
        fp.write("<div class=\"hashbox\">")
        fp.write("<h3>Current Hash</h3><div>")
        fp.write("<img src=\"\\assets\\hash\\map.png\" class=\"hash-image\">")
        fp.write("<img src=\"\\assets\\hash\\map.png\" class=\"hash-image\">")
        fp.write("<img src=\"\\assets\\hash\\none.png\" class=\"hash-image\">")
        fp.write("<img src=\"\\assets\\hash\\none.png\" class=\"hash-image\">")
        fp.write("<img src=\"\\assets\\hash\\none.png\" class=\"hash-image\">")
        fp.write("</div></div></p>")

        # Write the leaderboard
        fp.write("<ol class=\"player-table\">")
        fp.write("<span class=\"table-header\"><h4>RSL Season 3</h4></span>")
        for player, place in zip(leaderboard, range(len(leaderboard))):
            fp.write(f"<li class=\"table\">")
            fp.write(f"<span class=\"placement\">{tools.pretty_placement(int(1+place))}</span>")
            fp.write(f"<span class=\"player-name-leaderboard\">{tools.name_with_link(player)}</span>")
            fp.write(f"<span class=\"rating\">{player.display_rating}</span>")
            fp.write(f"<span class=\"race-deetz\">")
            fp.write(f"<span class=\"finishes\">{tools.should_i_plural('Finish', int(player.finishes))}</span>")
            fp.write(f"<span class=\"race-count\">{tools.should_i_plural('Race', int(player.forfeits+player.finishes))}</span>")
            fp.write(f"</span>")
            fp.write(f"</li>")
        fp.write("</ol></p>")

        # Write the table of unqualified players
        fp.write("<ol class=\"player-table\">")
        fp.write("<span class=\"table-header unranked-table\"><h4>Unranked Players</h4><h4>3 Total Finishes Needed</h4></span>")
        for player in unqualed:
            fp.write(f"<li class=\"table unranked-table\">")
            fp.write(f"<span class=\"unranked-name\">{tools.name_with_link(player)}</span>")
            fp.write(f"<span class=\"unranked-remaining\">{tools.should_i_plural('Finish', 3-player.finishes)} to Qualify</span>")
        fp.write("</ol>")

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
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/rasyncs.css\">")
        fp.write("<script src=\"/scripts/toggle_element.js\"></script>")

        # Write the body
        for race in racelist[::-1]:
            fp.write(race.htmltable)
            fp.write("</p>")

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            footer = fin.read()
        fp.write(footer)


def generated_rated_asyncs(racelist):
    with open("public/rasyncs.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            header = fin.read()
        fp.write(header) 
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/rasyncs.css\">")
        fp.write("<script src=\"/scripts/toggle_element.js\"></script>")

        # Write the body
        for race in racelist[::-1]:
            if race.slug[:11] != 'Rated Async':
                continue
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


def generate_html_weights():
    settinglist = weights.download_weights()

    with open("public/weights.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            header = fin.read()
        fp.write(header)
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/weights.css\">")
        fp.write("<script src=\"/scripts/toggle_element.js\"></script>")
        
        # Write the body
        fp.write('<ol class="setting-table">')
        for setting in settinglist:
            fp.write(setting.htmlblock)
        fp.write('</ol>')

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            footer = fin.read()
        fp.write(footer)