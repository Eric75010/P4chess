import random


class Tournament:
    def generate_pairs_for_a_round(self, round_number, players_selected):
        pairs = []
        random.shuffle(players_selected)
        for i in range(0, len(players_selected), 2):
            if i + 1 < len(players_selected):
                pairs.append((players_selected[i], players_selected[i + 1]))
            else:
                print(f"The player {players_selected[i].name} is waiting for another player")
        print(f"Pairs generated for the round {round_number +1}.")
        print(pairs)

        return pairs


players = [
    {
        "id": "CC12345",
        "name": "bill",
        "firstname": "kill",
        "date_of_birth": "06072000"
    },
       {
        "id": "AV12345",
        "name": "tim",
        "firstname": "det",
        "date_of_birth": "06092100"
    },
    {
        "id": "BZ12345",
        "name": "ric",
        "firstname": "jim",
        "date_of_birth": "09082010"
    },
    {
        "id": "UU12345",
        "name": "jill",
        "firstname": "tily",
        "date_of_birth": "06072000"
    },
        {
        "id": "AH12345",
        "name": "marcel",
        "firstname": "pro",
        "date_of_birth": "06072012"
    },
            {
        "id": "AH54321",
        "name": "celo",
        "firstname": "amro",
        "date_of_birth": "06072020"
    }
]

tournament = Tournament()

round_number = 1
pairs = tournament.generate_pairs_for_a_round(round_number, players)