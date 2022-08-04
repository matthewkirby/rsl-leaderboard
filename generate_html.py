import tools
import weights
from datetime import datetime

def generate_website(leaderboard, unqualed, racelist):
    generate_html_leaderboard(leaderboard, unqualed)
    generate_html_racelist(racelist)
    generated_rated_asyncs(racelist)
    generate_html_weights()
    generate_resources()
    generate_rules()


def generate_html_leaderboard(leaderboard, unqualed):
    with open("public/index.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html") as fin:
            fp.write(fin.read())

        # Write the tournament information
        # fp.write("<ol class=\"player-table\">")
        # fp.write("<span class=\"table-header\"><h4>Season 4 Tournament Information</h4></span>")
        # fp.write("<li class=\"table\"><span class=\"resource-element\">")
        # fp.write("<a href=\"https://docs.google.com/spreadsheets/d/1IyXCCq0iowzCoUH7mB8oSduiQU6QqLY6LE1nJEKUOMs\" class=\"table\">Swiss Pairings</a>")
        # fp.write("</span></li>")
        # fp.write("<li class=\"table\"><span class=\"resource-element\">")
        # fp.write("<a href=\"https://docs.google.com/spreadsheets/d/1LRJ3oo_2AWGq8KpNNclRXOq4OW8O7LrHra7uY7oQQlA/edit#gid=1920581233\" class=\"table\">Race Schedule</a>")
        # fp.write("</span></li>")
        # fp.write("</ol></p>")

        # Write the leaderboard
        fp.write("<ol class=\"player-table\">")
        fp.write("<span class=\"table-header\"><h4>RSL Season 4</h4></span>")
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
        fp.write("</ol></p>")

        nowtime = datetime.now().strftime("%H:%M:%S %b %-d, %Y")
        fp.write(f"<div class=\"last-update-date\">Last Updated: {nowtime}</div>")

        # Close out tags
        with open("html_templates/closeout.html") as fin:
            fp.write(fin.read())

def generate_html_racelist(racelist):
    with open("public/racelist.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            fp.write(fin.read())
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/rasyncs.css\">")
        fp.write("<script src=\"/scripts/toggle_element.js\"></script>")

        # Write the body
        for race in racelist[::-1]:
            fp.write(race.htmltable)
            fp.write("</p>")

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            fp.write(fin.read())


def generated_rated_asyncs(racelist):
    with open("public/rasyncs.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            fp.write(fin.read())
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
            fp.write(fin.read())


def generate_resources():
    with open("public/resources.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            fp.write(fin.read())

        # Write the body
        with open("html_templates/resource_body.html", 'r') as fin:
            fp.write(fin.read())

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            fp.write(fin.read())


def generate_rules():
    with open("public/rules.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            fp.write(fin.read())

        # Write the body
        with open("html_templates/rules_body.html", 'r') as fin:
            fp.write(fin.read())

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            fp.write(fin.read())


def generate_html_weights():
    settinglist = weights.download_weights()

    with open("public/weights.html", 'w') as fp:
        # Write the header
        with open("html_templates/preamble.html", 'r') as fin:
            fp.write(fin.read())
        fp.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/weights.css\">")
        fp.write("<script src=\"/scripts/toggle_element.js\"></script>")
        
        # Write the body
        fp.write('<ol class="setting-table">')
        for setting in settinglist:
            fp.write(setting.htmlblock)
        fp.write('</ol>')

        # Close out tags
        with open("html_templates/closeout.html", 'r') as fin:
            fp.write(fin.read())
