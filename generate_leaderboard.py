import os, sys
import trueskill
from racetime_api_call import fetch_race
import generate_html as ghtml
from race import Race
from player import Player

# Todo: Clicking on a players rating (or entire cell) will bring you to a page with a table that contains each race slug and the delta rating
# Todo: Make a page of tables of races. Shows players in order of placement, before ratings, and rating delta
# Todo: Header to link between race table and leaderboard


def print_leaderboard(leaderboard, fp=sys.stdout):
    sep = '\t' if fp == sys.stdout else ','
    header = ['Ranking', 'Name', 'Rating', 'Finishes', 'Forfeits']
    print(*header, sep=sep, file=fp)
    for player, i in zip(leaderboard, range(len(leaderboard))):
        line = [str(i+1), player.display_name, player.display_rating, player.finishes, player.forfeits]
        print(*line, sep=sep, file=fp)


def main():
    # Fetch missing racetime race data
    asynclist = [asyn.strip() for asyn in open("asynclist.txt", 'r')]
    sluglist = [slug.strip() for slug in open("sluglist.txt", 'r')]
    for slug in sluglist:
        fetch_race(slug)

    # Load the racetime races
    racefnames = ["races/"+slug+".json" for slug in sluglist] + ["other_races/"+slug+".json" for slug in asynclist]
    racelist = [Race(fname) for fname in racefnames]

    # Sort the races in order of date
    racelist.sort(key=lambda race: race.datetime)

    # Maintain a list of players, adding new players as they appear in races
    global_playerlist = {}
    for race in racelist:
        playerlist, placement = [], []
        for player in race.entrants:
            if player['userid'] not in global_playerlist:
                global_playerlist[player['userid']] = Player(player['userid'], player['display_name'])

            playerlist.append(global_playerlist[player['userid']])
            placement.append(player['place'])

        # Count the race for each player
        for player, place in zip(playerlist, placement):
            player.count_race(place)

        # Put forfeits in last place
        ffplace = 1 + max([x for x in placement if x is not None])
        placement = [x if x is not None else ffplace for x in placement]

        # Compute ratings for the race
        race.rate(playerlist, placement)

    # Finalize the rankings
    global_playerlist = [player for _, player in global_playerlist.items()]
    global_playerlist.sort(key=lambda player: player.display_rating, reverse=True)


    # Print and save rankings to a file
    print_leaderboard(global_playerlist)
    with open("leaderboard.txt", 'w') as lbout:
        print_leaderboard(global_playerlist, lbout)
    ghtml.generate_html_leaderboard(global_playerlist)
    ghtml.generate_html_racelist(racelist)


if __name__ == "__main__":
    main()