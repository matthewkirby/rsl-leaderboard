# RSL Leaderboard
This repo is designed to calculate ratings and generate a leaderboard using TrueSkill. This basically mimics racetime.gg's built-in leaderboard but allows us to have more power over races. The driving motive behind this code base was to enable async races being included in the seasonal ratings.

## Dependencies
- We require both the requests package and the trueskill package to run. These can be installed through pip: `pip3 install trueskill requests`

## Usage
Anyone can generate the ratings at home! Just run `generate_leaderboard.py`. This will fetch all of missing race data from racetime for each slug listed in `sluglist.txt`, order both racetime races and async races in time, and then calculate ratings.

To include additional races, just add their racetime.gg slugs to `sluglist.txt`. You can add races not on racetime by copying and editing the template, `async_races/async_template.json` and adding the name of the file to `asyncslist.txt`. For example, if you made a new race and put it in the file `async_races/async1a.json`, you would add `async1a` to `asynclist.txt`.