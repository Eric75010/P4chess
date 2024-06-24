import os.path
import random
from datetime import datetime

from PlayerView import PlayerView
from model import Player, Tournament, Match, Round
from view import MainView, UserManagementView, ReportView, RunTournamentView
import json


class Controller:
    """
    Main controller class to manage the overall application flow.
    """

    def __init__(self):
        """
        Initialize the Controller with necessary views and controllers
        """
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.run_tournament_controller = RunTournamentController(
            RunTournamentView(), PlayerView()
        )
        self.tournaments = []
        self.report_view = ReportView()
        self.load_tournaments_from_json()

    def user_management(self):
        """
        Manage the creation, update and delete players.
        """
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
            self.leave_program()
        elif user_select == "5":
            self.player_controller.display_players()

    def load_tournaments_from_json(self):
        """
        Load tournaments from a JSON file.
        """
        filename = "tournaments.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    tournament_list = json.load(f)
                    for tournament_data in tournament_list:
                        tournament = Tournament(
                            tournament_data["tournament_name"],
                            tournament_data["place"],
                            datetime.fromisoformat
                            (tournament_data["start_date"]),
                            datetime.fromisoformat
                            (tournament_data["end_date"]),
                            tournament_data["description"],
                            tournament_data["round_number"],
                        )
                        player_set = set()
                        for round_data in tournament_data.get("rounds", []):
                            round_instance = Round(round_data["name"])
                            for match_data in round_data.get("matches", []):
                                player1_name = match_data["player1"]
                                player2_name = match_data["player2"]
                                player1 = self.get_or_create_player(
                                    player1_name)
                                player2 = self.get_or_create_player(
                                    player2_name)
                                player_set.update([player1, player2])
                                match = Match(player1=player1, player2=player2)
                                match.result = match_data["result"]
                                round_instance.add_match(match)
                            tournament.add_round(round_instance)
                        tournament.registered_players = list(player_set)
                        self.tournaments.append(tournament)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {filename}: {e}")
        else:
            print("No tournament data found.")

    def get_or_create_player(self, name):
        """
        Retrieve an existing player by name or create a new one if not found.

        :param name: The name of the player.
        :type name: str
        :return: The player object.
        :rtype: Player
        """
        player = self.get_player_by_name(name)
        if not player:
            player = player(name=name, firstname="", date_of_birth="", id=name)
            self.player_controller.players.append(player)
        return player

    def get_player_by_name(self, name):
        """
        Find a player by his name.

        :param name: The name of the player.
        :type name: str
        :return: The player object if found, None otherwise.
        :rtype: Player or None
        """
        for player in self.player_controller.players:
            if player.name == name:
                return player
        return None

    def reports(self):
        """
        Display various reports based on user selection.
        """
        report_view = ReportView()
        report_view.display_report_submenu()
        report_option = self.main_view.get_selected_option()

        if report_option == "1":
            self.player_controller.load_players_from_json("players.json")
            all_players = self.remove_duplicates(
                self.player_controller.players)
            sorted_players = sorted(all_players, key=lambda p: p.name)
            self.report_view.display_tournament_players_by_alphabetical_order(
                sorted_players
            )
        elif report_option == "2":
            self.report_view.display_all_tournaments(self.tournaments)
        elif report_option == "3":
            tournament_name = input("Enter the name of the tournament: ")
            report_view.display_tournament_info(tournament_name)
        elif report_option == "4":
            tournament_name = input("Enter the name of the tournament: ")
            found_tournament = next(
                (t for t in self.tournaments
                 if t.tournament_name == tournament_name),
                None,
            )
            if found_tournament:
                sorted_players = sorted(
                    found_tournament.registered_players,
                    key=lambda p: p.name)
                (self.report_view.display_tournament_players_by_alphabetical_order(  # noqa: E501
                    sorted_players))
            else:
                self.report_view.display_tournament_not_found()
        elif report_option == "5":
            tournament_name = input(
                "Enter the name of the tournament: ")
            found_tournament = next(
                (t for t in self.tournaments
                 if t.tournament_name == tournament_name), None)
            if found_tournament:
                self.report_view.display_tournament_rounds_and_matches(
                    found_tournament)
            else:
                self.report_view.display_tournament_not_found()
        else:
            print("Invalid option, select again")

    def remove_duplicates(self, players):
        """
        Remove duplicate players from a list.

        :param players: a list of player objects.
        :type players: list
        :return: A list of unique player objects.
        :rtype: list
        """
        unique_players = {}
        for player in players:
            if player.id not in unique_players:
                unique_players[player.id] = player
        return list(unique_players.values())

    def run(self):
        """
        Main method to run the program.
        """
        while True:
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
                break
            else:
                print("Invalid option, please try again.")

    def leave_program(self):
        """
        Method to leave the program.
        """
        self.main_view.display_leave_program_message()
        confirmation = self.main_view.confirm_leave_the_program()
        if confirmation:
            print("exiting the program!.")
            exit()
        else:
            print("Resuming the program.")

    def display_players_from_json(self):
        """
        Display players from a JSON file.
        """
        with open("players.json", "r") as f:
            players_data = json.load(f)
            sorted_players = sorted(players_data,
                                    key=lambda player: player["name"])
            print("List of players from players.json:")
            for player in sorted_players:
                print(
                    f"ID: {player['id']},"
                    f" Name: {player['name']},"
                    f"  Firstname: {player['firstname']},"
                    f" Date of birth : {player['date_of_birth']}"
                )

    def display_tournaments_from_json(self):
        """
        Display tournaments from a JSON file.
        """
        print("Data from tournaments.json")
        with open("tournaments.json") as f:
            tournaments_data = json.load(f)

        print("List of tournaments from tournaments.json")
        for tournament in tournaments_data:
            print(f"Tournament name: {tournament['tournament_name']}")
            print(f"Place: {tournament['place']}")
            print(f"Start date: {tournament['start_date']}")
            print(f"End date: {tournament['end_date']}")
            print(f"Round number: {tournament['round_number']}")
            print(f"Description: {tournament['description']}")
            if "matches" in tournament:
                print(f"Matches: {tournament['matches']}")
            else:
                print("No matches available for this tournament")

            print()

    def display_tournament_details(self, tournament_name):
        """
        Display the details of a specific tournament.

        :param tournament_name: The name of the tournament.
        :type tournament_name: str
        """
        print("Data from tournaments.json")
        with open("tournaments.json") as f:
            tournaments_data = json.load(f)

        for tournament in tournaments_data:
            if tournament["tournament_name"] == tournament_name:
                print("Tournament details:")
                print(f"Tournament name: {tournament['tournament_name']}")
                print(f"Place: {tournament['place']}")
                print(f"Start date: {tournament['start_date']}")
                print(f"End date: {tournament['end_date']}")
                print(f"Round number: {tournament['round_number']}")
                print(f"Description: {tournament['description']}")
                if "matches" in tournament:
                    print("matches:")
                    for match in tournament["matches"]:
                        print(
                            f"Round {match['round_number']}:"
                            f" {match['player1']} vs {match['player2']}"
                        )
                else:
                    print("No matches available for this tournament")
                break
        else:
            print("Tournament not found!")


class PlayerController:
    """
    Controller class to manage player actions.
    """

    def __init__(self):
        """
        Initialize the PlayerController with necessary views and datas.
        """
        self.player_view = PlayerView()
        self.players = []
        self.load_players_from_json("players.json")

    def create_player(self):
        """
        Create a new player by input from the user.
        """

        id = self.player_view.ask_id()
        name = self.player_view.ask_name()
        firstname = self.player_view.ask_firstname()
        date_of_birth = self.player_view.ask_date_of_birth()
        new_player = Player(
            id=id, name=name, firstname=firstname, date_of_birth=date_of_birth)
        self.players.append(new_player)
        self.save_players_to_json("players.json")
        self.player_view.display_player(name, firstname, date_of_birth)

    def display_players(self):
        """
        Display the list of players.
        """
        print("Players list:")
        self.player_view.display_players(self.players)

    def update_player_by_id(self, player_id):
        """
        Update player information based on ID.

        :param player_id: The ID of the player to update.
        :type player_id: str
        """
        player_to_update = next(
            (player for player in self.players if player.id == player_id), None
        )

        if player_to_update:
            name = self.player_view.ask_name()
            firstname = self.player_view.ask_firstname()
            date_of_birth = self.player_view.ask_date_of_birth()

            player_to_update.name = name
            player_to_update.firstname = firstname
            player_to_update.date_of_birth = date_of_birth

            self.save_players_to_json("players.json")
            print("Player updated with success!")
        else:
            print("Player not found!")

    def delete_player_by_id(self, player_id):
        """
        Delete a player based on ID.

        :param player_id: The ID of the player to delete.
        :type player_id: str
        """
        player_to_delete = next(
            (player for player in self.players if player.id == player_id), None
        )

        if player_to_delete:
            self.players.remove(player_to_delete)
            self.save_players_to_json(player_to_delete)
            print("Player deleted with success!")
        else:
            print("Player not found!")

    def save_players_to_json(self, filename):
        """
        Save the list of players to a JSON file.

        :param filename: The name of the file to save the players.
        :type filename: str
        """
        data = [
            {
                "id": player.id,
                "name": player.name,
                "firstname": player.firstname,
                "date_of_birth": player.date_of_birth,
            }
            for player in self.players
        ]

        with open(filename, "w+") as f:
            json.dump(data, f, indent=4)

    def load_players_from_json(self, filename):
        """
        Load players from a JSON file.

        :param filename: The name of the file to load the players from.
        :type filename: str
        """
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                for player_data in data:
                    if "id" in player_data:
                        self.players.append(
                            Player(
                                player_data["name"],
                                player_data["firstname"],
                                player_data["date_of_birth"],
                                player_data["id"],
                            )
                        )
                    else:
                        print("Player 'id' is missing")
        else:
            print("no player data found.")


class RunTournamentController:
    """
    Controller class to manage tournament actions.
    """

    def __init__(self, tournament_view, player_view):
        """
        Initialize the RunTournamentController with necessary views and datas.

        :param tournament_view: The view for tournament actions.
        :type tournament_view: RunTournamentView
        :param player_view: The view for player actions.
        :type player_view: PlayerView
        """
        self.tournaments = []
        self.player_controller = PlayerController()
        self.tournament_players = []
        self.rounds = []
        self.previous_round_pairs = {}
        self.tournament_view = tournament_view
        self.player_view = player_view
        self.report_view = ReportView()

    def create_tournament(self):
        """
        Method to create a new tournament.
        """
        tournament_details = self.tournament_view.display_create_tournament()

        tournament = Tournament(
            tournament_details["name"],
            tournament_details["place"],
            tournament_details["start date"],
            tournament_details["end date"],
            tournament_details["description"],
            int(tournament_details["round number"]),
        )

        self.tournaments.append(tournament)
        self.player_view.display_players(self.player_controller.players)
        self.add_players_to_tournament(tournament)

        print("Tournament created with success!")
        print("Tournament name:", tournament.tournament_name)
        print(f"Start date:, {tournament.start_date}")

        for round_number in range(1, tournament.round_number + 1):
            # print(f"\nStarting round {round_number}")
            round_instance = Round(round_number)
            if round_number == 1:
                pairs = self.generate_pairs_for_first_round(tournament)
            else:
                pairs = self.generate_pair_by_score(
                    tournament.registered_players, tournament.played_matches
                )

            self.display_pairs(
                pairs, round_number)
            self.record_matches(pairs, tournament, round_instance)
            tournament.add_round(round_instance)
            if round_number < tournament.round_number:
                print(
                    f"\nRound {round_number} completed."
                    f" Preparing for round {round_number + 1}..."
                )

        self.save_tournaments_to_json("tournaments.json")

        self.report_view.display_tournament_rounds_and_matches(tournament)
        print("*" * 20)

    def add_players_to_tournament(self, tournament):
        """
        Add players to a tournament.

        :param tournament: The tournament to add players to.
        :type tournament: Tournament
        """
        ids = self.tournament_view.add_players_to_tournament()
        for player_id in ids:
            if player_id:
                player = next(
                    (p for p in self.player_controller.players
                     if p.id == player_id),
                    None,
                )
                if player:
                    tournament.registered_players.append(player)
                    print(player)
                else:
                    print(f"Player with ID {player_id} not found.")

    def record_match_result(self, match, winner=None, loser=None, draw=False):
        """
        Record  the  result of a match.

        :param match: the match to record the result for.
        :type match: Match
        :param winner: The player who won the match, defaults to None.
        :type winner: Player, optional
        :param loser: The player who lost the match, defaults to None.
        :type loser: Player, optional
        :param draw: Indicates if the was draw, defaults to False.
        :type draw: bool, optional
        :return: The match with the recorded result.
        :rtype: Match
        """
        if draw:
            match.result = ([match.player1, 0.5], [match.player2, 0.5])
        else:
            if winner and loser:
                match.result = ([winner, 1], [loser, 0])
        return match

    def generate_pairs_for_first_round(self, tournament):
        """
        Generate pairs of players for the first round of the tournament.

        :param tournament: The tournament where the pairs are generated.
        :type tournament: Tournament
        :return: A list of pairs of players.
        :rtype: list
        """
        players = tournament.registered_players
        random.shuffle(players)
        pairs = []
        for i in range(0, len(players) - 1, 2):
            pairs.append((players[i], players[i + 1]))
        if len(players) % 2 != 0:
            print(f"The player"
                  f" {players[-1].name} is waiting for another player!")
        return pairs

    def generate_pair_by_score(self, players, previous_round_pairs):
        """
        Generate pairs of players based on their scores.

        :param players: The list of players.
        :type players: list
        :param previous_round_pairs: the pairs from previous rounds.
        :type previous_round_pairs: list
        :return: A list of pairs of players.
        :rtype: list
        """
        players = [
            player for player in players if player is not None]
        player_by_scores = sorted(
            players, key=lambda x: x.points, reverse=True)

        pairs = []
        paired_players = set()

        for i in range(len(player_by_scores)):
            if player_by_scores[i] in paired_players:
                continue

            for j in range(i + 1, len(player_by_scores)):
                if player_by_scores[j] in paired_players:
                    continue

                new_pair = (player_by_scores[i], player_by_scores[j])
                if not self.has_played_before(new_pair, previous_round_pairs):
                    pairs.append(new_pair)
                    paired_players.add(player_by_scores[i])
                    paired_players.add(player_by_scores[j])
                    break

        unpaired_players = [
            player for player in player_by_scores
            if player not in paired_players]
        if len(unpaired_players) == 1:
            print(f"The player {unpaired_players[0].name}"
                  f" is waiting for another player!")

        return pairs

    def has_played_before(self, pair, played_matches):
        """
        Check if the players in a pair have played against each other before.

        :param pair: The pair of players.
        :type pair: tuple
        :param played_matches: The list of matches
         that have already been played.
        :type played_matches: list
        :return: True if the players have played before, False otherwise.
        :rtype: bool
        """
        for match in played_matches:
            if (match.player1.id == pair[0].id
                and match.player2.id == pair[1].id) or (
                match.player1.id == pair[1].id
                and match.player2.id == pair[0].id
            ):
                return True
        return False

    def generate_pairs_for_a_round(self, tournament, round_number):
        """
        Generate pairs of players for a round in the tournament.

        :param tournament: The tournament where the pairs are generated.
        :type tournament: Tournament
        :param round_number: The current round number.
        :type round_number: int
        :return: A list of pairs of players.
        :rtype: list
        """
        players = tournament.registered_players
        print(players)
        random.shuffle(players)
        pairs = []
        paired_players = set()

        if round_number == 1:
            for i in range(0, len(players), 2):
                print(players[i])
                if (
                    players[i] not in paired_players
                    and players[i + 1] not in paired_players
                ):
                    pairs.append((players[i], players[i + 1]))
                    paired_players.add((players[i], players[i + 1]))

            if (len(players) % 2 != 0
                    and players[-1] not in paired_players):
                print(f"The player {players[-1].name}"
                      f" is waiting for another player")
        else:
            pairs = self.generate_pair_by_score(
                players, tournament.played_matches)

        self.previous_round_pairs[round_number] = pairs

        return pairs

    def display_pairs(self, pairs, round_number):
        """
        Display the pairs generated for a round.

        :param pairs: the list of pairs.
        :type pairs: list
        :param round_number: the current round number.
        :type round_number: int
        :return:
        """
        print(f"\nStarting  round {round_number}")
        print(f"Pairs generated for round {round_number}:\n")
        for pair in pairs:
            print(f"Match: {pair[0].name} ({pair[0].id})"
                  f" vs {pair[1].name} ({pair[1].id})")
        print()

    def record_matches(self, pairs, tournament, round_instance):
        """
        Record the results of matches in a round.

        :param pairs: the list of pairs of players.
        :type pairs: list
        :param tournament: The tournament where the matches are recorded.
        :type tournament: Tournament
        :param round_instance: The current round instance.
        :type round_instance: Round
        """
        for pair in pairs:
            match = Match(pair[0], pair[1])
            # Affiche le match
            print(
                f"\nMatch: {pair[0].name} ({pair[0].id})"
                f" vs {pair[1].name} ({pair[1].id})")
            (winner, loser,
             draw) = self.input_match_scores(match)
            self.update_player_scores(winner, loser, draw)
            match = self.record_match_result(match, winner, loser, draw)
            round_instance.add_match(match)
            # Affiche le résultat du match
            if draw:
                print("Match nul!")
            else:
                if winner:
                    print(f"{winner.name} a gagné!")
                if loser:
                    print(f"{loser.name} a perdu!")
            print()
        tournament.add_round(round_instance)

    def display_round_matches(self, round_instance):
        """
        Display the matches in a round.

        :param round_instance: The current round instance.
        :type round_instance: Round
        """
        print(f"{round_instance.name} - Matches:")
        for match in round_instance.matches:
            print(f"Match: {match.player1.name} vs {match.player2.name}")

    def input_match_scores(self, match):
        """
        Input the scores for a match.

        :param match: the match to input scores for.
        :type match: Match
        :return: The winner, the loser and draw status.
        :rtype: tuple
        """
        draw = input("draw ? (yes/no): ").strip().lower()
        if draw == "yes":
            return None, None, True

        winner_id = input("Enter winner player id: ").strip()
        loser_id = input("Enter loser player id: ").strip()

        winner = self.get_player_for_id(
            self.player_controller.players, winner_id)
        loser = self.get_player_for_id(
            self.player_controller.players, loser_id)
        return winner, loser, False

    def update_player_scores(self, winner, loser, draw):
        """
        Update the scores of players based on the match result.

        :param winner: The player who won the match.
        :type winner: Player
        :param loser: The player who lost the match.
        :type loser: Player
        :param draw: Indicates if the match was a draw.
        :type draw: bool
        """
        if draw:
            if winner is not None and loser is not None:
                winner.update_points("draw")
                loser.update_points("draw")
        else:
            if winner is not None:
                winner.update_points("win")
            if loser is not None:
                loser.update_points("lose")

    def get_player_for_id(self, players, player_id):
        """
        Get a player by ID.

        :param players: The list of players.
        :type players: list
        :param player_id: The ID of the player.
        :type player_id: str
        :return: The player object if found, None otherwise.
        :rtype: Player or None
        """
        player_found = next(
            (player for player in players if player.id == player_id), None
        )
        return player_found

    def save_tournaments_to_json(self, filename):
        """
        Save the tournaments to a JSON file.

        :param filename: The name of the file to save the tournaments.
        :type filename: str
        """
        data = []
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Erreur de découpage JSON: {e}")
                os.rename(filename, filename + ".corrupted")

        for tournament in self.tournaments:
            tournament_data = {
                "tournament_name": tournament.tournament_name,
                "place": tournament.place,
                "start_date": tournament.start_date.isoformat(),
                "end_date": tournament.end_date.isoformat(),
                "round_number": tournament.round_number,
                "description": tournament.description,
                "rounds": [],  # liste pour les tours
                "players": [
                    {"id": player.id, "name": player.name}
                    for player in tournament.registered_players
                ],
            }

            for round_instance in tournament.rounds:
                round_data = {"name": round_instance.name, "matches": []}
                for match in round_instance.matches:
                    match_data = {
                        "player1": match.player1.name,
                        "player2": match.player2.name,
                        "result": match.result,
                    }
                    round_data["matches"].append(match_data)
                tournament_data["rounds"].append(round_data)

            if not any(
                t["tournament_name"] ==
                tournament.tournament_name for t in data
            ):
                data.append(tournament_data)

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    controller = Controller()
    controller.run()
