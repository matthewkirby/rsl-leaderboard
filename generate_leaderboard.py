import os, sys
import glob
import random
import trueskill
from racetime_api_call import fetch_race, download_sluglist
from generate_html import generate_website
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
    random.seed(69420)
    # Fetch missing racetime race data
    asynclist = [asyn.strip() for asyn in open("asynclist.txt", 'r')]
    races_to_fetch = [slug.strip() for slug in open("sluglist.txt", 'r')] + download_sluglist()
    for slug in races_to_fetch:
        fetch_race(slug)

    # Load the race data
    racelist = [Race(race_fname) for race_fname in glob.glob("races/**.json")]
    racelist += [Race("other_races/"+slug+".txt", asyn=True) for slug in asynclist]

    # Sort the races in order of date
    racelist.sort(key=lambda race: race.datetime)

    # Maintain a list of players, adding new players as they appear in races
    global_playerlist = {}
    for race in racelist:
        playerlist, forfeit_playerlist, placement = [], [], []
        for player in race.entrants:
            if player['userid'] not in global_playerlist:
                global_playerlist[player['userid']] = Player(player['userid'], player['display_name'])

            if player['place'] is None:
                forfeit_playerlist.append(global_playerlist[player['userid']])
            else:
                playerlist.append(global_playerlist[player['userid']])
            placement.append(player['place'])

        # Count the race for each player
        random.shuffle(forfeit_playerlist)
        playerlist += forfeit_playerlist
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

    # Split off anyone not qualified
    unqualed, leaderboard = [], []
    for player in global_playerlist:
        if player.finishes == 0:
            continue
        elif player.finishes < 3:
            unqualed.append(player)
        else:
            leaderboard.append(player)
        
    unqualed.sort(key=lambda player: player.display_name.upper())


    # Print and save rankings to a file
    print_leaderboard(global_playerlist)
    with open("leaderboard.txt", 'w') as lbout:
        print_leaderboard(global_playerlist, lbout)
    generate_website(leaderboard, unqualed, racelist)


if __name__ == "__main__":
    main()