import json

class Race:
    def __init__(self, filepath):
        with open(filepath, 'r') as fin:
            data = json.load(fin)

        self.slug = data['slug']
        self.datetime = data["ended_at"]
        self.entrants = [{
                "userid": entr['user']['id'],
                "place": entr['place'],
                "display_name": entr['user']['name']
            } for entr in data['entrants']]
