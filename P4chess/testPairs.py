

def generate_pair_by_score(self, round_number, players_selected, previous_round_pairs):
    # Récupérer les scores des joueurs
    players_selected = [player for player in players_selected if player is not None]
    player_scores = [(player, player.points) for player in players_selected]
    # trier la liste des joueurs par score
    sorted_players = sorted(player_scores, key=lambda x: x[1], reverse=True)
    # generer les paires
    pairs = []
    opponents_history = {player: set() for player in players_selected}

    i = 0
    print(sorted_players)
    while i < len(sorted_players):
        print("while!")
        if i + 1 < len(sorted_players):
            player1, player2 = sorted_players[i][0], sorted_players[i + 1][0]
            print(f"{player1=}")
            print(f"{player2=}")
            new_pair = (player1, player2)
            if new_pair not in previous_round_pairs \
                    and player2 not in opponents_history[player1] \
                    and player1 not in opponents_history[player2]:
                pairs.append(new_pair)
                opponents_history[player1].add(player2)
                opponents_history[player2].add(player1)
                i += 2  # nouvelle paire
            else:
                print(f"The pair {new_pair} has already been played, generating a new pair!")
                i += 1  # nouvelle paire
        else:
            print(f" {sorted_players[i][0].name} is waiting for another player")
            i += 1
    print(f"Pairs generated for the round {round_number + 1}.")
    print(pairs)
    return pairs

"""
    def generate_pairs_for_a_round(self, round_number, players_selected):
        pairs = []
        random.shuffle(players_selected)
        for i in range(0, len(players_selected), 2):
            if i + 1 < len(players_selected):
                pairs.append((players_selected[i], players_selected[i + 1]))
            else:
                print(f"The player {players_selected[i].name} is waiting for another player")
        print(f"Pairs generated for the round {round_number + 1}.")

        return pairs
"""