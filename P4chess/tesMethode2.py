import random

class Tournament:
    def generate_pair_by_score(self, round_number, players_selected, previous_round_pairs):
        # Récupérer les scores des joueurs
        players_selected = [player for player in players_selected if player is not None]
        player_scores = [(player.points, player) for player in players_selected]
        # trier la liste des joueurs par score
        sorted_players = sorted(player_scores, key=lambda x: x[0], reverse=True)
        # generer les paires
        pairs = []
        opponents_history = {player.id: set() for player in players_selected}

        i = 0
        print(sorted_players)
        while i < len(sorted_players):
            print("while!")
            if i + 1 < len(sorted_players):
                player1, player2 = sorted_players[i][1], sorted_players[i + 1][1]
                print(f"{player1=}")
                print(f"{player2=}")
                new_pair = (player1, player2)
                if new_pair not in previous_round_pairs \
                        and player2.id not in opponents_history[player1.id] \
                        and player1.id not in opponents_history[player2.id] :
                    pairs.append(new_pair)
                    opponents_history[player1.id].add(player2.id)
                    opponents_history[player2.id].add(player1.id)
                    i += 2 #nouvelle paire
                else:
                    print(f"The pair {new_pair} has already been played, generating a new pair!")
                    i += 1 #nouvelle paire
            else:
                print(f" {sorted_players[i][0].name} is waiting for another player")
                i +=1
        print(f"Pairs generated for the round {round_number + 1}.")
        print(pairs)
        return pairs


    def generate_pairs_for_a_round(self, round_number, players_selected):
        print("****")
        print(players_selected)
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
        "date_of_birth": "06072000",
        "points": 5
    },
       {
        "id": "AV12345",
        "name": "tim",
        "firstname": "det",
        "date_of_birth": "06092100",
        "points": 4

    },
        {
        "id": "BZ12345",
        "name": "ric",
        "firstname": "jim",
        "date_of_birth": "09082010",
        "points": 2
    },
        {
        "id": "UU12345",
        "name": "jill",
        "firstname": "tily",
        "date_of_birth": "06072000",
        "points": 10
    },
        {
        "id": "AH12345",
        "name": "marcel",
        "firstname": "pro",
        "date_of_birth": "06072012",
        "points": 7
    },
        {
        "id": "AH54321",
        "name": "celo",
        "firstname": "amro",
        "date_of_birth": "06072020",
        "points": 12
    },
]

tournament = Tournament()

round_number = 2
previous_round_pairs = []
pairs_by_score = tournament.generate_pairs_for_a_round(round_number, players)
print("pairs score:" )
print(pairs_by_score)

pairs_for_round = tournament.generate_pairs_for_a_round(round_number, players)
print("\nPaires sans scores")
print(pairs_for_round)
