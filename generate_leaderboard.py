from racetime_api_call import fetch_race
from race import Race
from player import Player
import trueskill


def compute_rating(playerlist, placement):
    """ Given a list of players and race placement, compute ratings using trueskill """
    ratings = [(player.rating,) for player in playerlist]
    ratings = trueskill.rate(ratings, ranks=placement)
    for i in range(len(ratings)):
        playerlist[i].rating = ratings[i][0]
        playerlist[i].compute_display_rating()
    


def main():
    # Fetch missing race data
    sluglist = [slug.strip() for slug in open("sluglist.txt", 'r')]
    for slug in sluglist:
        fetch_race(slug)

    # Load asyncs
    # asynclist = [asyn.strip() for asyn in open("asynclist.txt", 'r')]

    # Load the races and order them, earliest first
    racefnames = ["races/"+slug+".json" for slug in sluglist]
    racefnames = racefnames
    racelist = [Race(fname) for fname in racefnames]
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

        # Put forfeits in last place
        ffplace = 1 + max([x for x in placement if x is not None])
        placement = [x if x is not None else ffplace for x in placement]

        # Compute ratings for the race
        compute_rating(playerlist, placement)

    # Finalize and output the rankings
    global_playerlist = [player for _, player in global_playerlist.items()]
    global_playerlist.sort(key=lambda player: player.display_rating, reverse=True)
    for player, i in zip(global_playerlist, range(len(global_playerlist))):
        print(f"{i+1}.\t {player.display_name}\t{player.display_rating}")

if __name__ == "__main__":
    main()