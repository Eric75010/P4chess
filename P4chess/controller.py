import os.path
from fileinput import filename
import random

from PlayerView import PlayerView
from model import Player, Tournament, Match, Round
from view import MainView, UserManagementView, ReportView, RunTournamentView
import json


class Controller:
    def __init__(self):
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.run_tournament_controller = RunTournamentController()
        self.tournaments = []
        self.report_view = ReportView(self.tournaments)


    def user_management(self):
        # Gestion des utilisateurs
        user_management_view = UserManagementView()
        user_management_view.display_menu()
        user_select = input("select an option: ")
        # print(f"{user_select=}")
        if user_select == "1":
            self.player_controller.create_player()
        elif user_select == "2":
            player_id = user_management_view.update_player()
            self.player_controller.update_player_by_id(player_id)
        elif user_select == "3":
            player_id = user_management_view.delete_player()
            self.player_controller.delete_player_by_id(player_id)
        elif user_select == "4":
            self.leave_the_program()
        elif user_select == "5":
            self.player_controller.display_players()

    def load_tournaments_from_json(self):
        # Charge les tournois depuis un fichier JSON
        filename = "tournaments.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                tournament_list = json.load(f)
                for tournament_data in tournament_list:
                    self.tournaments.append(
                        Tournament(tournament_data["tournament_name"],
                                   tournament_data["place"],
                                   tournament_data["start_date"],
                                   tournament_data["end_date"],
                                   tournament_data["round_number"],
                                   tournament_data["description"]))
        else:
            print("no player data found.")

    def reports(self):
        # Affiche les rapports
        report_view = ReportView(self.tournaments)
        report_view.display_report_submenu()
        report_option = self.main_view.get_selected_option()

        if report_option == "1":
            self.display_players_from_json()
            #report_view.display_tournament_players_by_alphabetical_order(tournament_name)
        elif report_option == "2":
            self.display_tournaments_from_json()
            #report_view.display_all_tournaments()
        elif report_option == "3":
            tournament_name = input("Enter the name of the tournament: ")
            report_view.display_tournament_info(tournament_name)
        elif report_option == "4":
            tournament_name = input("Enter the name of the tournament: ")
            self.report_view.display_tournament_players_by_alphabetical_order(tournament_name)
        elif report_option == "5":
            tournament_name = input("Enter the name of the tournament: ")
            report_view.display_tournament_rounds_and_matches(tournament_name)
        else:
            print("Invalid option, select again")

    def display_players_from_json(self):
        with open('players.json', 'r') as f:
            # Charge les noms depuis le fichier json
            players_data = json.load(f)
            # Tri la liste des joueurs par leur nom
            sorted_players = sorted(players_data, key=lambda player: player['name'])
            # Affiche les infos de chaque joueur
            print("List of players from players.json:")
            for player in sorted_players:
                print(f"ID: {player['id']}, Name: {player['name']},  Firstname: {player['firstname']}, Date of birth : {player['date_of_birth']}")

    def display_tournaments_from_json(self):
        print("Data from tournaments.json")
        # Charge les données des tournois depuis le fichier json
        with open('tournaments.json') as f:
            tournaments_data = json.load(f)

        # Affiche les infos de chaque tournoi
        print("List of tournaments from tournaments.json")
        for tournament in tournaments_data:
            print(f"Tournament name: {tournament['tournament_name']}")
            print(f"Place: {tournament['place']}")
            print(f"Start date: {tournament['start_date']}")
            print(f"End date: {tournament['end_date']}")
            print(f"Round number: {tournament['round_number']}")
            print(f"Description: {tournament['description']}")

            if 'matches' in tournament:
                print(f"Matches: {tournament['matches']}")
            else:
                print("No matches available for this tournament")

            print()

    def display_tournament_details(self, tournament_name):
        print("Data from tournaments.json")
        # Charge les données des tournois depuis le fichier json
        with open('tournaments.json') as f:
            tournaments_data = json.load(f)

        # Recherche le tournoi par son nom
        for tournament in tournaments_data:
            if tournament['tournament_name'] == tournament_name:
                print("Tournament details:")
                print(f"Tournament name: {tournament['tournament_name']}")
                print(f"Place: {tournament['place']}")
                print(f"Start date: {tournament['start_date']}")
                print(f"End date: {tournament['end_date']}")
                print(f"Round number: {tournament['round_number']}")
                print(f"Description: {tournament['description']}")

                if 'matches' in tournament:
                    print("matches:")
                    for match in tournament['matches']:
                        print(f"Round {match['round_number']}: {match['player1']} vs {match['player2']}")
                else:
                    print("No matches available for this tournament")
                break
        else:
            print("Tournament not found!")




    def run(self):
        # Méthode principale pour exécuter le programme
        self.main_view.display_menu()
        user_select = self.main_view.get_selected_option()
        if user_select == "1":
            self.run_tournament_controller.create_tournament()
        elif user_select == "2":
            self.user_management()
        elif user_select == "3":
            self.reports()
        elif user_select == "4":
            self.leave_program()


    def leave_program(self):
        # Méthode pour quitter le programme
        self.main_view.display_leave_program_message()
        confirmation = self.main_view.confirm_leave_the_program()
        if confirmation:
            print("exiting the program!.")
        else:
            print("Resuming the program.")


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()
        self.players = []
        self.load_players_from_json("players.json")


    def create_player(self):
        # Créer unnouveau joueur
        id = self.player_view.ask_id()
        name = self.player_view.ask_name()
        firstname = self.player_view.ask_firstname()
        date_of_birth = self.player_view.ask_date_of_birth()
        new_player = Player(name, firstname, date_of_birth, id)
        self.players.append(new_player)
        self.save_player_to_json(new_player)
        print(new_player)

    def display_players_list(self):
        # Affiche la liste des joueurs
        print("Players list:")
        for player in self.players:
            print(f"Id: {player.id}, Name: {player.name}, Firstname: {player.firstname}, Date of birth: {player.date_of_birth}")


    def update_player_by_id(self, player_id):
        # Mise à jour des informations des joueur à partir de l'id
        player_to_update = None
        for player in self.players:
            if player.id == player_id:
                player_to_update = player
                break

        if player_to_update:
            name = self.player_view.ask_name()
            firstname = self.player_view.ask_firstname()
            date_of_birth = self.player_view.ask_date_of_birth()

            player_to_update.name = name
            player_to_update.firstname = firstname
            player_to_update.date_of_birth = date_of_birth

            print("Player updated wwith success!")
        else:
            print("Player not found!")

    def delete_player_by_id(self, player_id):
        # Efface un joueur sélectionné par son id
        player_to_delete = None
        print("players")
        for player in self.players:
            print(f"check player id: {player.id}")
        for player in self.players:
            print(f"player id: {player.id}")
            if player.id == player_id:
                player_to_delete = player
                break

        if player_to_delete:
            self.players.remove(player_to_delete)
            print("Player deleted with success!")
            self.save_player_to_json(player_to_delete)
        else:
            print("Player not found!")


    def save_player_to_json(self, player: Player):
        # Sauvegarde les données d'un joueur dans un fichier JSON
        filename = "players.json"
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)
        with open(filename, 'r') as openfile:
            json_object = json.load(openfile)
        updated_data = [p for p in json_object if p["id"] != player.id]
        updated_data.append({
            "id": player.id,
            "name": player.name,
            "firstname": player.firstname,
            "date_of_birth": player.date_of_birth
        })
        with open(filename, 'w+') as f:
            json.dump(updated_data, f, indent = 4)


    def save_players_to_json(self, filename):
        # Sauvegarde une liste de joueurs dans un fichier JSPN
        data = []
        for player in self.players:
            data.append({
                "id": player.id,
                "name": player.name,
                "firstname": player.firstname,
                "date_of_birth": player.date_of_birth
            })
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_players_from_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                for player_data in data:
                    if "id" in player_data:
                        self.players.append(Player(player_data["name"], player_data["firstname"], player_data["date_of_birth"], player_data["id"]))
                    else:
                        print("Player 'id' is missing")
        else:
            print("no player data found.")

class RunTournamentController:
    def __init__(self):
        #self.tournament = Tournament()
        self.tournaments = []
        self.player_controller = PlayerController()
        self.tournament_players = []
        self.rounds = []
        self.previous_round_pairs = {}

    def get_player_for_id(self, players, player_id):
        player_found = None
        for player in players:
            if player.id == player_id:
                player_found = player
                break
        return player_found

    def get_previous_round_pairs(self, round_number):
        return self.previous_round_pairs.get(round_number, [])

    def create_tournament(self):
        # Méthode pour créer un tournoi
        run_tournament_view = RunTournamentView()
        tournament_details = run_tournament_view.display_create_tournament()
        actual_number_round = 0
        tournament_rounds = []
        rounds = []
        registered_players = []

        new_tournament = Tournament(tournament_details["name"],
                                    tournament_details["place"],
                                    tournament_details["start date"],
                                    tournament_details["end date"],
                                    tournament_details["description"],
                                    int(tournament_details["round number"]),
                                    )

        self.tournaments.append(new_tournament)
        self.save_tournaments_to_json("tournaments.json")

        print("Tournament created with success!")
        print("Tournament name:", new_tournament.tournament_name)
        print("Start date:", new_tournament.start_date)

        self.player_controller.display_players_list()
        ids = run_tournament_view.add_players_to_tournament()

        for id in ids:
            player_found = self.get_player_for_id(self.player_controller.players, id)
            if player_found is not None:
                self.tournament_players.append(player_found)

        print("Players added to the tournament.")


        current_tournament = self.tournaments[-1]
        #debug
        #import pdb;pdb.set_trace()
        for round_number in range(1, current_tournament.round_number +1):
            current_round = Round(round_number)
            if round_number == 1:
                pairs = self.generate_pairs_for_a_round(round_number)
            else:
                previous_round_pairs = self.get_previous_round_pairs(round_number - 1)
                pairs = self.generate_pair_by_score(round_number, self.tournament_players, previous_round_pairs)

            print(f"\nRound {round_number + 1} - Matches:")
            # Matchs
            for index, pair in enumerate(pairs):
                if pair[0] is not None and pair[1] is not None:
                    print(f"Match {index + 1}: {pair[0].name} vs {pair[1].name}")
                else:
                    print(f"Match {index + 1}: A player is waiting for another player")

                print(f"Match {pair[0]}")
                print(f"Match {pair[1]}")

                print(f"Match {index + 1}: {pair[0].name} vs {pair[1].name}")
            updated_matches = []

            for match_number, pair in enumerate(pairs):
                match = Match(pair[0], pair[1])

                winner, loser, draw = self.input_match_scores(match)
                self.update_player_scores(winner, loser, draw)
                updated_match = self.record_match_result(match)
                updated_matches.append(updated_match)

            current_round.matches = updated_matches
            current_tournament.rounds.append(current_round)

        self.player_controller.save_player_to_json("players.json")
        self.generate_tournament_summary(current_tournament.round_number)

    def record_match_result(self, match, winner=None, loser=None, draw=False):
        # Enregistre le résultat d'un match
        if draw:
            print("Match nul!")
            players = ([match.player1, 0.5], [match.player2, 0.5])
        else:
            players = None
            if winner and loser:
                print(f"{winner.name} a gagné!")
                players = ([winner, 1], [loser, 0])
        #return players
        match.players = players
        return match

    def generate_pair_by_score(self, round_number, players_selected, previous_round_pairs):
        # Méthode pour générer des paires en fonction des scores
        # Récupérer les scores des joueurs
        players_selected = [player for player in players_selected if player is not None]
        player_scores = [(player.points, player) for player in players_selected]
        # trier la liste des joueurs par score
        sorted_players = sorted(player_scores, key=lambda x: x[0], reverse=True)
        # generer les paires
        pairs = []
        opponents_history = {player.id: set() for player in players_selected}

        i = 0
        while i < len(sorted_players):
            if i + 1 < len(sorted_players):
                player1, player2 = sorted_players[i][1], sorted_players[i + 1][1]
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
        return pairs


    def generate_pairs_for_a_round(self, round_number):
        # Méthode poour générer des paires de joueurs pour un tour
        pairs = []
        random.shuffle(self.tournament_players)
        for i in range(0, len(self.tournament_players), 2):
            if i + 1 < len(self.tournament_players):
                pairs.append((self.tournament_players[i], self.tournament_players[i + 1]))
            else:
                print(f"The player {self.tournament_players[i].name} is waiting for another player")
        print(f"Pairs generated for the round {round_number +1}.")
        print(pairs)

        return pairs

    def input_match_scores(self, match):
        # Méthode pour saisir les scores des matchs
        winner_id = input("Enter winner player id: ")
        loser_id = input("Enter loser player id: ")
        draw = input("draw ? (yes/no): ")

        #Récuperer les objets joueur correspondants aux identifiants
        winner = self.get_player_for_id(self.tournament_players, winner_id)
        loser = self.get_player_for_id(self.tournament_players, loser_id)
        return winner, loser, draw
    def update_player_scores(self, winner, loser, draw):
        #Méthode pour mettre à jour le scor des joueurs
        # Mise à jour des points des joueurs
        if draw.lower() == "yes":
            # Ajout de 0.5 point si match nul
            winner.points += 0.5
            loser.points += 0.5
        else:
            # Ajout d'un point au gagnant
            winner.points += 1
            loser.points += 0

    def generate_tournament_summary(self, round):
        # Méthode pour générer un résumé du tournoi
        pass

    def save_tournaments_to_json(self, filename):
        # Méthode pour sauvegarder les tournois au format JSON
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
        else:
            data = []


        tournament_data = {
                "tournament_name": self.tournaments[-1].tournament_name,
                "place": self.tournaments[-1].place,
                "start_date": self.tournaments[-1].start_date.isoformat(),
                "end_date": self.tournaments[-1].end_date.isoformat(),
                "round_number": self.tournaments[-1].round_number,
                "description": self.tournaments[-1].description,
                "matches" : [] #liste pour les matchs
        }

        for round in self.tournaments[-1].rounds:
            for match in round.matches:
                match_data = {
                    "player1": match.player1.name,
                    "player2": match.player2.name
                    # ajout infos
                }
                tournament_data["matches"].append(match_data)
        data.append(tournament_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    controller = Controller()
    controller.run()
